import sys
import math
from typing import Any, Dict, Mapping, Optional, Tuple
from datetime import datetime, timedelta
import json

import backoff
import msal
import requests
from requests import session
from simplejson import JSONDecodeError
from requests.exceptions import (
    Timeout,
    ConnectionError as RequestsConnectionError,
    ChunkedEncodingError
)
from singer import get_logger, metrics

from tap_ms_dynamics_365_crm.xml_transformer import transform_metadata_xml
from tap_ms_dynamics_365_crm.exceptions import (
    ERROR_CODE_EXCEPTION_MAPPING,
    MSDynamics365CrmError,
    MSDynamics365CrmRateLimitError,
    MSDynamics365CrmUnprocessableEntityError,
    MSDynamics365CrmInternalServerError,
    MSDynamics365CrmNotImplementedError,
    MSDynamics365CrmBadGatewayError,
    MSDynamics365CrmServiceUnavailableError
)

LOGGER = get_logger()
REQUEST_TIMEOUT = 300
API_VERSION = "9.2"
MAX_PAGESIZE = 5000
MAX_RETRIES = 5
REFRESH_URL = "https://login.microsoftonline.com/common/oauth2/token"
CLIENT_CREDENTIALS_AUTHORITY_URL = "https://login.microsoftonline.com/{tenant_id}"
DEFAULT_EXPIRY_TIME_IN_SECONDS = 3600
USER_AGENT = "Singer Tap MS Dynamics 365 CRM"
AUTH_METHOD_AUTHORIZATION_CODE = "authorization_code"
AUTH_METHOD_CLIENT_CREDENTIALS = "client_credentials"

def raise_for_error(response: requests.Response) -> None:
    """Raises the associated response exception. Takes in a response object,
    checks the status code, and throws the associated exception based on the
    status code.

    :param resp: requests.Response object
    """
    try:
        response_json = response.json()
    except Exception:
        LOGGER.warning("Failed to parse JSON from response. Response text.")
        response_json = {}

    if response.status_code not in [200, 201, 204]:
        # Try to extract error message from various possible locations in response
        error_message = None
        error_code = None

        # Check for error object (common in MS Dynamics responses)
        if isinstance(response_json, dict):
            error_obj = response_json.get("error")
            if isinstance(error_obj, dict):
                error_message = error_obj.get("message")
                error_code = error_obj.get("code")
            elif isinstance(error_obj, str):
                error_message = error_obj
        else:
            error_message = str(response_json)

        # Fallback to default error message
        if not error_message:
            error_message = ERROR_CODE_EXCEPTION_MAPPING.get(
                response.status_code, {}
            ).get("message", "Unknown Error")

        # Build final message
        if error_code:
            message = f"HTTP-error-code: {response.status_code}, Error Code: {error_code}, Error: {error_message}"
        else:
            message = f"HTTP-error-code: {response.status_code}, Error: {error_message}"

        exc = ERROR_CODE_EXCEPTION_MAPPING.get(response.status_code, {}).get(
            "raise_exception", MSDynamics365CrmError
        )
        raise exc(message, response) from None

def retry_after_wait_gen():
    """
    Generator function to retrieve 'Retry-After' header from the exception response and
    sleep for the specified time.
    This is used in the backoff decorator to handle rate limiting (HTTP 429) errors.
    The generator runs indefinitely - the backoff decorator controls when to stop via max_tries.
    """
    DEFAULT_WAIT_TIME = 60

    # Generator yields indefinitely; backoff decorator controls termination via max_tries
    while True:
        exc_info = sys.exc_info()
        sleep_time = DEFAULT_WAIT_TIME

        # Try to extract Retry-After header from the exception response
        if exc_info[1] is not None and hasattr(exc_info[1], 'response'):
            resp = exc_info[1].response
            if resp and hasattr(resp, 'headers'):
                sleep_time_str = resp.headers.get('Retry-After')
                if sleep_time_str:
                    try:
                        parsed_sleep_time = math.floor(float(sleep_time_str))
                        if parsed_sleep_time > 0:
                            sleep_time = parsed_sleep_time
                            LOGGER.info(f'API rate limit exceeded -- sleeping for '
                                        f'{sleep_time} seconds')
                        else:
                            LOGGER.warning(f'Invalid Retry-After value: {sleep_time_str}, '
                                           f'using default {DEFAULT_WAIT_TIME}s')
                    except (ValueError, TypeError):
                        LOGGER.warning(f'Could not parse Retry-After header: {sleep_time_str}, '
                                       f'using default {DEFAULT_WAIT_TIME}s')

        yield sleep_time


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
        raw_auth_method = config.get("auth_method")
        if raw_auth_method is None or raw_auth_method == "":
            self.auth_method = AUTH_METHOD_AUTHORIZATION_CODE
        elif not isinstance(raw_auth_method, str):
            raise ValueError(
                "Invalid auth_method type: expected string, "
                f"got {type(raw_auth_method).__name__}."
            )
        else:
            self.auth_method = raw_auth_method.strip().lower()
        self.tenant_id = config.get("tenant_id")
        self.refresh_token = config.get("refresh_token")
        self.api_version = API_VERSION
        self.max_pagesize = config.get("max_pagesize", MAX_PAGESIZE)
        self.start_date = config.get("start_date")
        self.user_agent = config.get("user_agent", USER_AGENT)

        self._access_token = None
        self._expires_at = None

        self._session = session()
        self.base_url = f"{self.organization_uri}/api/data/v{self.api_version}"

        # Handle request_timeout with validation
        config_request_timeout = config.get("request_timeout")
        if config_request_timeout is not None:
            try:
                timeout_value = float(config_request_timeout)
            except (ValueError, TypeError) as e:
                raise ValueError(
                    f"Invalid request_timeout value: '{config_request_timeout}'. "
                    f"Must be a positive number."
                ) from e

            if timeout_value <= 0:
                raise ValueError(
                    f"Invalid request_timeout value: {timeout_value}. "
                    f"Must be greater than 0."
                )
            self.request_timeout = timeout_value
        else:
            self.request_timeout = REQUEST_TIMEOUT

    def __enter__(self):
        self.check_api_credentials()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._session.close()

    def check_api_credentials(self) -> None:
        allowed_auth_methods = [AUTH_METHOD_AUTHORIZATION_CODE, AUTH_METHOD_CLIENT_CREDENTIALS]

        if not self.organization_uri:
            raise ValueError("organization_uri is required and cannot be null or empty")
        if not self.client_id:
            raise ValueError("client_id is required and cannot be null or empty")
        if self.request_timeout <= 0:
            raise ValueError("request_timeout must be greater than 0")
        if self.auth_method not in allowed_auth_methods:
            raise ValueError(
                f"Invalid auth_method: '{self.auth_method}'. "
                f"Supported values are: {AUTH_METHOD_AUTHORIZATION_CODE}, {AUTH_METHOD_CLIENT_CREDENTIALS}."
            )

        if self.auth_method == AUTH_METHOD_AUTHORIZATION_CODE:
            if not self.client_secret:
                raise ValueError(
                    "client_secret is required when auth_method is authorization_code"
                )
            if not self.refresh_token:
                raise ValueError(
                    "refresh_token is required when auth_method is authorization_code"
                )

        if self.auth_method == AUTH_METHOD_CLIENT_CREDENTIALS:
            if not self.tenant_id:
                raise ValueError(
                    "tenant_id is required when auth_method is client_credentials"
                )

            if not self.client_secret:
                raise ValueError(
                    "client_secret is required when auth_method is client_credentials"
                )

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

    def _client_credentials_scope(self) -> str:
        organization_uri = self.organization_uri.rstrip("/")
        return f"{organization_uri}/.default"

    def _acquire_access_token_client_credentials(self) -> None:
        """Acquires access token using OAuth client credentials flow."""
        LOGGER.info("Acquiring Access Token with client_credentials flow")

        authority = CLIENT_CREDENTIALS_AUTHORITY_URL.format(tenant_id=self.tenant_id)
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=authority,
            client_credential=self.client_secret
        )

        result = app.acquire_token_for_client(scopes=[self._client_credentials_scope()])
        if "access_token" not in result:
            error = result.get("error")
            error_description = result.get("error_description")
            correlation_id = result.get("correlation_id")
            raise MSDynamics365CrmError(
                "Failed to acquire access token using client_credentials. "
                f"error={error}, description={error_description}, correlation_id={correlation_id}"
            )

        self._access_token = result["access_token"]
        expires_in_seconds = result.get("expires_in", DEFAULT_EXPIRY_TIME_IN_SECONDS)
        self._expires_at = datetime.now() + timedelta(seconds=int(expires_in_seconds) - 10)
        LOGGER.info("Got access token using client_credentials flow")

    def get_access_token(self) -> str:
        """Return access token if available or generate one."""
        if self._access_token and self._expires_at and self._expires_at > datetime.now():
            return self._access_token

        if self.auth_method == AUTH_METHOD_CLIENT_CREDENTIALS:
            self._acquire_access_token_client_credentials()
        else:
            self._refresh_access_token()
        return self._access_token

    def _get_standard_headers(self):
        """Return standard headers for API request."""
        return {
            "Authorization": "Bearer {}".format(self.get_access_token()),
            "User-Agent": self.user_agent,
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
            "If-None-Match": "null",
            "Content-Type": "application/json"
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
        endpoint: str = None,
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

        # Use json parameter for POST/PATCH to properly serialize body
        kwargs = {
            "headers": headers,
            "params": params,
            "timeout": self.request_timeout
        }
        if method.upper() in ("POST", "PATCH", "PUT") and body:
            kwargs["json"] = body

        return self.__make_request(method, endpoint, **kwargs)

    @backoff.on_exception(
        wait_gen=retry_after_wait_gen,
        exception=(
            MSDynamics365CrmRateLimitError,
        ),
        max_tries=MAX_RETRIES,
        jitter=None
    )
    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(
            ConnectionResetError,
            RequestsConnectionError,
            ChunkedEncodingError,
            Timeout,
            MSDynamics365CrmUnprocessableEntityError,
            MSDynamics365CrmInternalServerError,
            MSDynamics365CrmNotImplementedError,
            MSDynamics365CrmBadGatewayError,
            MSDynamics365CrmServiceUnavailableError
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
            if method in ("GET", "POST", "PATCH", "PUT", "DELETE"):
                response = self._session.request(method, endpoint, **kwargs)
                raise_for_error(response)
            else:
                raise ValueError(f"Unsupported method: {method}")

        try:
            results = response.json()
        except JSONDecodeError:
            results = response.text

        return results
