import unittest
import requests
from unittest.mock import patch, Mock
from parameterized import parameterized
from requests.exceptions import Timeout, ConnectionError, ChunkedEncodingError
from datetime import datetime, timedelta
from tap_ms_dynamics_365_crm.client import (
    Client,
    raise_for_error,
    retry_after_wait_gen,
    AUTH_METHOD_CLIENT_CREDENTIALS,
    AUTH_METHOD_AUTHORIZATION_CODE
)
from tap_ms_dynamics_365_crm.exceptions import (
    MSDynamics365CrmError,
    MSDynamics365CrmBadRequestError,
    MSDynamics365CrmUnauthorizedError,
    MSDynamics365CrmForbiddenError,
    MSDynamics365CrmNotFoundError,
    MSDynamics365CrmConflictError,
    MSDynamics365CrmUnprocessableEntityError,
    MSDynamics365CrmInternalServerError,
    MSDynamics365CrmNotImplementedError,
    MSDynamics365CrmBadGatewayError,
    MSDynamics365CrmServiceUnavailableError,
    MSDynamics365CrmRateLimitError,
)


default_config = {
    "organization_uri": "https://api.example.com",
    "request_timeout": 30,
    "client_id": "test_client",
    "client_secret": "test_secret",
    "auth_method": "authorization_code",
    "redirect_uri": "http://localhost",
    "refresh_token": "test_refresh",
    "max_pagesize": 5000,
    "start_date": "2024-01-01T00:00:00Z"
}

DEFAULT_REQUEST_TIMEOUT = 300

class MockResponse:
    """Mocked standard HTTPResponse to test error handling."""

    def __init__(
        self, status_code, resp="", content=None, headers=None, raise_error=True, text=None, json_data=None
    ):
        self.json_data = resp
        self.status_code = status_code
        self.content = content if content is not None else [""]
        self.headers = headers or {}
        self.raise_error = raise_error
        self.text = text if text is not None else {}
        self._json_data = json_data if json_data is not None else self.text
        self.reason = "error"

    def raise_for_status(self):
        """If an error occur, this method returns a HTTPError object.

        Raises:
            requests.HTTPError: Mock http error.

        Returns:
            int: Returns status code if not error occurred.
        """
        if not self.raise_error:
            return self.status_code

        raise requests.HTTPError("mock sample message")

    def json(self):
        """Returns a JSON object of the result."""
        return self._json_data

class TestClient(unittest.TestCase):

    def setUp(self):
        """Set up the client with default configuration."""
        self.client = Client(config_path="config.json", config=default_config)

    @parameterized.expand([
        ["string value", "12", 12.0, False],
        ["integer value", 10, 10.0, False],
        ["float value", 20.0, 20.0, False],
        ["empty value", "", None, True],
        ["zero value", 0, None, True]
    ])
    @patch("tap_ms_dynamics_365_crm.client.session")
    def test_client_initialization(self, test_name, input_value, expected_value, should_raise, mock_session):
        test_config = default_config.copy()
        test_config["request_timeout"] = input_value

        if should_raise:
            with self.assertRaises(ValueError):
                client = Client(config_path="config.json", config=test_config)
        else:
            client = Client(config_path="config.json", config=test_config)
            assert client.request_timeout == expected_value
            assert isinstance(client._session, mock_session().__class__)

    @parameterized.expand([
        ["400 error", 400, MSDynamics365CrmBadRequestError, "Bad request. The request URL or body is invalid or malformed."],
        ["401 error", 401, MSDynamics365CrmUnauthorizedError, "Unauthorized. The access token is missing, expired, or invalid."],
        ["403 error", 403, MSDynamics365CrmForbiddenError, "Forbidden. The user does not have the required Dataverse security role or privilege to perform this operation."],
        ["404 error", 404, MSDynamics365CrmNotFoundError, "Not found. The requested resource or entity record does not exist."],
        ["409 error", 409, MSDynamics365CrmConflictError, "Conflict. The operation conflicts with an existing record (duplicate detection or concurrency violation)."],
    ])
    def test_make_request_http_failure_without_retry(self, test_name, error_code, error, error_message):
        mock_response = MockResponse(error_code, json_data={})
        with patch.object(self.client._session, "request", return_value=mock_response):
            with self.assertRaises(error) as e:
                self.client._Client__make_request("GET", "https://api.example.com/resource")

        expected_error_message = f"HTTP-error-code: {error_code}, Error: {error_message}"
        self.assertEqual(str(e.exception), expected_error_message)

    @parameterized.expand([
        ["422 error", 422, MSDynamics365CrmUnprocessableEntityError, "Unprocessable entity. The request was well-formed but could not be processed."],
        ["500 error", 500, MSDynamics365CrmInternalServerError, "Internal server error. The server encountered an unexpected condition which prevented it from fulfilling the request."],
        ["501 error", 501, MSDynamics365CrmNotImplementedError, "Not implemented. The server does not support the functionality required to fulfill the request."],
        ["502 error", 502, MSDynamics365CrmBadGatewayError, "Bad gateway. An upstream proxy or load balancer received an invalid response from the MS Dynamics server."],
        ["503 error", 503, MSDynamics365CrmServiceUnavailableError, "Service unavailable. The MS Dynamics 365 API service is temporarily unavailable. Retry after a short delay."],
    ])
    @patch("time.sleep")
    def test_make_request_http_failure_with_retry(self, test_name, error_code, error, error_message, mock_sleep):
        mock_response = MockResponse(error_code, json_data={})
        with patch.object(self.client._session, "request", return_value=mock_response) as mock_request:
            with self.assertRaises(error) as e:
                self.client._Client__make_request("GET", "https://api.example.com/resource")

            expected_error_message = f"HTTP-error-code: {error_code}, Error: {error_message}"
            self.assertEqual(str(e.exception), expected_error_message)
            self.assertEqual(mock_request.call_count, 5)

    @parameterized.expand([
        ["ConnectionResetError", ConnectionResetError],
        ["ConnectionError", ConnectionError],
        ["ChunkedEncodingError", ChunkedEncodingError],
        ["Timeout", Timeout],
    ])
    @patch("time.sleep")
    def test_make_request_other_failure_with_retry(self, test_name, error, mock_sleep):
        with patch.object(self.client._session, "request", side_effect=error) as mock_request:
            with self.assertRaises(error):
                self.client._Client__make_request("GET", "https://api.example.com/resource")

            self.assertEqual(mock_request.call_count, 5)

    def test_raise_for_error_with_error_code(self):
        """Test error handling with MS Dynamics error code format"""
        error_response = MockResponse(
            403,
            json_data={"error": {"code": "0x80040220", "message": "Principal user missing privileges"}}
        )
        with self.assertRaises(MSDynamics365CrmForbiddenError) as e:
            raise_for_error(error_response)

        self.assertIn("0x80040220", str(e.exception))
        self.assertIn("Principal user missing privileges", str(e.exception))

    def test_raise_for_error_with_string_error(self):
        """Test error handling when error is a string"""
        error_response = MockResponse(500, json_data={"error": "Internal server error"})
        with self.assertRaises(MSDynamics365CrmInternalServerError) as e:
            raise_for_error(error_response)

        self.assertIn("Internal server error", str(e.exception))

    def test_raise_for_error_success_status(self):
        """Test that no error is raised for successful responses"""
        for status_code in [200, 201, 204]:
            response = MockResponse(status_code, json_data={})
            try:
                raise_for_error(response)
            except Exception:
                self.fail(f"raise_for_error raised exception for status {status_code}")

    @patch("time.sleep")
    def test_rate_limit_with_retry_after_header(self, mock_sleep):
        """Test rate limit handling with Retry-After header"""
        mock_response = MockResponse(
            429,
            headers={'Retry-After': '30'},
            json_data={}
        )
        with patch.object(self.client._session, "request", return_value=mock_response) as mock_request:
            with self.assertRaises(MSDynamics365CrmRateLimitError):
                self.client._Client__make_request("GET", "https://api.example.com/resource")

            self.assertEqual(mock_request.call_count, 5)

    def test_retry_after_wait_gen_with_response(self):
        """Test retry_after_wait_gen generator with valid response"""
        gen = retry_after_wait_gen()

        # First yield should be 60 (default, no exception)
        wait_time = next(gen)
        self.assertEqual(wait_time, 60)

    def test_make_request_with_path(self):
        """Test make_request with path parameter"""
        mock_response = MockResponse(200, json_data={"data": "success"})
        with patch.object(self.client._session, "request", return_value=mock_response):
            with patch.object(self.client, "get_access_token", return_value="test_token"):
                result = self.client.make_request("GET", path="EntityDefinitions")
                self.assertEqual(result, {"data": "success"})

    def test_make_request_with_endpoint(self):
        """Test make_request with endpoint parameter"""
        mock_response = MockResponse(200, json_data={"data": "success"})
        with patch.object(self.client._session, "request", return_value=mock_response):
            with patch.object(self.client, "get_access_token", return_value="test_token"):
                result = self.client.make_request("GET", endpoint="https://api.example.com/test")
                self.assertEqual(result, {"data": "success"})

    @patch("tap_ms_dynamics_365_crm.client.open", create=True)
    @patch("json.dump")
    @patch("json.load")
    def test_write_config(self, mock_json_load, mock_json_dump, mock_open):
        """Test config writing on token refresh"""
        mock_json_load.return_value = default_config.copy()
        self.client._write_config("new_refresh_token")

        self.assertEqual(self.client.refresh_token, "new_refresh_token")
        mock_json_dump.assert_called_once()

    def test_check_api_credentials_missing_org_uri(self):
        """Test credential validation fails with missing organization_uri"""
        invalid_config = default_config.copy()
        invalid_config["organization_uri"] = ""
        client = Client(config_path="config.json", config=invalid_config)

        with self.assertRaises(ValueError) as e:
            client.check_api_credentials()
        self.assertIn("organization_uri", str(e.exception))

    def test_client_initialization_invalid_auth_method_type(self):
        invalid_config = default_config.copy()
        invalid_config["auth_method"] = 123

        with self.assertRaises(ValueError) as e:
            Client(config_path="config.json", config=invalid_config)

        self.assertIn("Invalid auth_method type", str(e.exception))

    def test_check_api_credentials_requires_tenant_for_client_credentials(self):
        invalid_config = default_config.copy()
        invalid_config["auth_method"] = AUTH_METHOD_CLIENT_CREDENTIALS
        invalid_config["tenant_id"] = ""
        client = Client(config_path="config.json", config=invalid_config)

        with self.assertRaises(ValueError) as e:
            client.check_api_credentials()

        self.assertIn("tenant_id is required", str(e.exception))

    def test_check_api_credentials_requires_secret_for_client_credentials(self):
        invalid_config = default_config.copy()
        invalid_config["auth_method"] = AUTH_METHOD_CLIENT_CREDENTIALS
        invalid_config["tenant_id"] = "tenant-id"
        invalid_config["client_secret"] = ""
        client = Client(config_path="config.json", config=invalid_config)

        with self.assertRaises(ValueError) as e:
            client.check_api_credentials()

        self.assertIn("client_secret is required", str(e.exception))

    def test_check_api_credentials_client_credentials_with_secret(self):
        valid_config = default_config.copy()
        valid_config["auth_method"] = AUTH_METHOD_CLIENT_CREDENTIALS
        valid_config["tenant_id"] = "tenant-id"
        valid_config["refresh_token"] = ""
        valid_config["redirect_uri"] = ""
        client = Client(config_path="config.json", config=valid_config)

        # Should not raise because client_secret + tenant_id are enough
        client.check_api_credentials()

    def test_check_api_credentials_auth_code_requires_refresh_token(self):
        invalid_config = default_config.copy()
        invalid_config["auth_method"] = AUTH_METHOD_AUTHORIZATION_CODE
        invalid_config["refresh_token"] = ""
        client = Client(config_path="config.json", config=invalid_config)

        with self.assertRaises(ValueError) as e:
            client.check_api_credentials()

        self.assertIn("refresh_token is required", str(e.exception))

    def test_get_access_token_uses_client_credentials_when_selected(self):
        self.client.auth_method = AUTH_METHOD_CLIENT_CREDENTIALS
        self.client._access_token = None
        self.client._expires_at = None

        with patch.object(self.client, "_acquire_access_token_client_credentials") as mock_client_credentials, \
                patch.object(self.client, "_refresh_access_token") as mock_refresh:
            mock_client_credentials.side_effect = lambda: setattr(self.client, "_access_token", "token")
            token = self.client.get_access_token()

        self.assertEqual(token, "token")
        mock_client_credentials.assert_called_once()
        mock_refresh.assert_not_called()

    def test_get_access_token_uses_cached_token(self):
        self.client._access_token = "cached-token"
        self.client._expires_at = datetime.now() + timedelta(minutes=10)

        with patch.object(self.client, "_acquire_access_token_client_credentials") as mock_client_credentials, \
                patch.object(self.client, "_refresh_access_token") as mock_refresh:
            token = self.client.get_access_token()

        self.assertEqual(token, "cached-token")
        mock_client_credentials.assert_not_called()
        mock_refresh.assert_not_called()

    def test_acquire_access_token_client_credentials_with_secret(self):
        self.client.auth_method = AUTH_METHOD_CLIENT_CREDENTIALS
        self.client.tenant_id = "tenant-id"
        self.client.client_secret = "secret"

        mock_app = Mock()
        mock_app.acquire_token_for_client.return_value = {"access_token": "token", "expires_in": 3600}
        with patch("tap_ms_dynamics_365_crm.client.msal.ConfidentialClientApplication", return_value=mock_app) as mock_cc_app:
            self.client._acquire_access_token_client_credentials()

        self.assertEqual(self.client._access_token, "token")
        self.assertIsNotNone(self.client._expires_at)
        mock_cc_app.assert_called_once()
        call_kwargs = mock_cc_app.call_args.kwargs
        self.assertEqual(call_kwargs["client_credential"], "secret")
        mock_app.acquire_token_for_client.assert_called_once_with(
            scopes=[self.client._client_credentials_scope()]
        )

    def test_acquire_access_token_client_credentials_failure_message(self):
        self.client.auth_method = AUTH_METHOD_CLIENT_CREDENTIALS
        self.client.tenant_id = "tenant-id"
        self.client.client_secret = "secret"

        mock_app = Mock()
        mock_app.acquire_token_for_client.return_value = {
                "error": "invalid_client",
                "error_description": "AADSTS7000215: Invalid client secret is provided."
            }
        with patch("tap_ms_dynamics_365_crm.client.msal.ConfidentialClientApplication", return_value=mock_app):
            with self.assertRaises(MSDynamics365CrmError) as exc:
                self.client._acquire_access_token_client_credentials()

        self.assertIn("invalid_client", str(exc.exception))
        self.assertIn("Invalid client secret", str(exc.exception))
