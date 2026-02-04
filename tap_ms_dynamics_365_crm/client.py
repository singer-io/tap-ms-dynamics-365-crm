from typing import Any, Dict, Mapping, Optional, Tuple
from datetime import datetime, timedelta
import json
import time

import backoff
import requests
from requests import session
from requests.exceptions import Timeout, ConnectionError, ChunkedEncodingError
from singer import get_logger, metrics

from tap_ms_dynamics_365_crm.exceptions import ERROR_CODE_EXCEPTION_MAPPING, MSDynamics365CrmError, MSDynamics365CrmBackoffError

LOGGER = get_logger()
REQUEST_TIMEOUT = 300
API_VERSION = "9.2"
MAX_PAGESIZE = 5000
MAX_RETRIES = 5
REFRESH_URL = "https://login.microsoftonline.com/common/oauth2/token"
DEFAULT_EXPIRY_TIME_IN_SECONDS = 3600
USER_AGENT = "Singer Tap MS Dynamics 365 CRM"

def raise_for_error(response: requests.Response) -> None:
    """Raises the associated response exception. Takes in a response object,
    checks the status code, and throws the associated exception based on the
    status code.

    :param resp: requests.Response object
    """
    try:
        response_json = response.json()
    except Exception:
        response_json = {}
    if response.status_code not in [200, 201, 204]:
        if response_json.get("error"):
            message = f"HTTP-error-code: {response.status_code}, Error: {response_json.get('error')}"
        else:
            error_message = ERROR_CODE_EXCEPTION_MAPPING.get(
                response.status_code, {}
            ).get("message", "Unknown Error")
            message = f"HTTP-error-code: {response.status_code}, Error: {response_json.get('message', error_message)}"
        exc = ERROR_CODE_EXCEPTION_MAPPING.get(response.status_code, {}).get(
            "raise_exception", MSDynamics365CrmError
        )
        raise exc(message, response) from None

class Client:
    """
    A Wrapper class.
    ~~~
    Performs:
     - Authentication
     - Response parsing
     - HTTP Error handling and retry
    """

    def __init__(self, config_path: str, config: Mapping[str, Any]) -> None:
        self.config_path = config_path
        self.config = config
        self.organization_uri = config.get("organization_uri")
        self.client_id = config.get("client_id")
        self.client_secret = config.get("client_secret")
        self.redirect_uri = config.get("redirect_uri")
        self.refresh_token = config.get("refresh_token")
        self.api_version = config.get("api_version", API_VERSION)
        self.max_pagesize = config.get("max_pagesize", MAX_PAGESIZE)
        self.start_date = config.get("start_date")
        self.user_agent = config.get("user_agent", USER_AGENT)

        self._access_token = None
        self._expires_at = None

        self._session = session()
        self.base_url = f"{self.organization_uri}/api/data/v{self.api_version}"
        self.request_timeout = float(config.get("request_timeout", REQUEST_TIMEOUT))

    def __enter__(self):
        self.check_api_credentials()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._session.close()

    def check_api_credentials(self) -> None:
        if not self.organization_uri:
            raise ValueError("organization_uri is required and cannot be null or empty")
        if not self.api_version:
            raise ValueError("api_version is required and cannot be null or empty")
        if self.request_timeout <= 0:
            raise ValueError("request_timeout must be greater than 0")

    def _write_config(self, refresh_token):
        """Writes updated refresh token to config file."""
        LOGGER.info("Credentials Refreshed")
        self.refresh_token = refresh_token

        # Update config at config_path
        with open(self.config_path) as file:
            config = json.load(file)

        config['refresh_token'] = refresh_token
        self.config['refresh_token'] = refresh_token

        with open(self.config_path, 'w') as file:
            json.dump(config, file, indent=2)

    def _refresh_access_token(self) -> None:
        """Refreshes the access token."""
        LOGGER.info("Refreshing Access Token")
        response = self._session.post(
            REFRESH_URL,
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': self.redirect_uri,
                'refresh_token': self.refresh_token,
                'grant_type': 'refresh_token',
                'resource': self.organization_uri
            }
        )

        if response.status_code != 200:
            raise MSDynamics365CrmError('Non-200 response fetching Dynamics access token')

        data = response.json()

        self._access_token = data.get("access_token")
        expires_in_seconds = data.get("expires_in", DEFAULT_EXPIRY_TIME_IN_SECONDS)

        if self.refresh_token != data.get('refresh_token'):
            self._write_config(data.get('refresh_token'))

        # pad by 10 seconds for clock drift
        self._expires_at = datetime.now() + timedelta(seconds=int(expires_in_seconds) - 10)
        LOGGER.info("Got refreshed access token")

    def get_access_token(self) -> str:
        """Return access token if available or generate one."""
        if self._access_token and self._expires_at > datetime.now():
            return self._access_token

        self._refresh_access_token()
        return self._access_token

    def _get_standard_headers(self):
        return {
            "Authorization": "Bearer {}".format(self.get_access_token),
            "User-Agent": self.user_agent,
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
            "If-None-Match": "null"
        }

    def authenticate(self, headers: Dict, params: Dict) -> Tuple[Dict, Dict]:
        """Authenticates the request with the token"""
        default_headers = self._get_standard_headers()
        if headers:
            headers = {**default_headers, **headers}
        else:
            headers = default_headers
        return headers, params

    def make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        path: Optional[str] = None
    ) -> Any:
        """
        Sends an HTTP request to the specified API endpoint.
        """
        params = params or {}
        headers = headers or {}
        body = body or {}
        endpoint = endpoint or f"{self.base_url}/{path}"
        headers, params = self.authenticate(headers, params)
        return self.__make_request(
            method, endpoint,
            headers=headers,
            params=params,
            data=body,
            timeout=self.request_timeout
        )

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(
            ConnectionResetError,
            ConnectionError,
            ChunkedEncodingError,
            Timeout,
            MSDynamics365CrmBackoffError
        ),
        max_tries=MAX_RETRIES,
        factor=2,
    )
    def __make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Optional[Mapping[Any, Any]]:
        """Performs HTTP Operations."""
        method = method.upper()
        with metrics.http_request_timer(endpoint):
            if method in ("GET", "POST"):
                if method == "GET":
                    kwargs.pop("data", None)
                response = self._session.request(method, endpoint, **kwargs)
                raise_for_error(response)
            else:
                raise ValueError(f"Unsupported method: {method}")

        return response.json()

