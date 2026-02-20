import json
import os
from pathlib import Path

from tap_tester.base_suite_tests.base_case import BaseCase


class MSDynamics365CRMBaseTest(BaseCase):
    """Setup expectations for test sub classes.

    Metadata describing streams. A bunch of shared methods that are used
    in tap-tester tests. Shared tap-specific methods (as needed).
    """
    start_date = "2019-01-01T00:00:00Z"
    PARENT_TAP_STREAM_ID = "parent-tap-stream-id"
    _expected_metadata_cache = None

    @staticmethod
    def tap_name():
        """The name of the tap."""
        return "tap-ms-dynamics-365-crm"

    @staticmethod
    def get_type():
        """The name of the tap."""
        return "platform.ms-dynamics-365-crm"

    @classmethod
    def expected_metadata(cls):
        """The expected streams and metadata about the streams."""
        if cls._expected_metadata_cache is not None:
            return cls._expected_metadata_cache

        metadata_path = Path(__file__).with_name("expected_metadata.json")
        if not metadata_path.exists():
            raise FileNotFoundError(
                f"Expected metadata file not found: {metadata_path}. "
                "Generate it from discovery output before running tests."
            )

        raw_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

        cls._expected_metadata_cache = {
            stream_name: {
                cls.PRIMARY_KEYS: set(stream_info.get("primary_keys", [])),
                cls.REPLICATION_METHOD: stream_info.get("replication_method", cls.INCREMENTAL),
                cls.REPLICATION_KEYS: set(stream_info.get("replication_keys", [])),
                cls.OBEYS_START_DATE: stream_info.get("obeys_start_date", True),
                cls.API_LIMIT: stream_info.get("api_limit", 100),
            }
            for stream_name, stream_info in raw_metadata.items()
        }

        return cls._expected_metadata_cache

    @staticmethod
    def get_credentials():
        """Authentication information for the test account."""
        credentials_dict = {}
        creds = {
            'client_id': 'TAP_MS_DYNAMICS_365_CRM_CLIENT_ID',
            'client_secret': 'TAP_MS_DYNAMICS_365_CRM_CLIENT_SECRET',
            'organization_uri': 'TAP_MS_DYNAMICS_365_CRM_ORGANIZATION_URI',
            'redirect_uri': 'TAP_MS_DYNAMICS_365_CRM_REDIRECT_URI',
            'refresh_token': 'TAP_MS_DYNAMICS_365_CRM_REFRESH_TOKEN',
        }

        for cred in creds:
            credentials_dict[cred] = os.getenv(creds[cred])

        return credentials_dict

    def get_properties(self, original: bool = True):
        """Configuration of properties required for the tap."""
        return_value = {
            "start_date": "2022-07-01T00:00:00Z",
            "page_size": 100
        }
        if original:
            return return_value

        return_value["start_date"] = self.start_date
        return return_value

    def expected_parent_tap_stream(self, stream=None):
        """return a dictionary with key of table name and value of parent stream"""
        parent_stream = {
            table: properties.get(self.PARENT_TAP_STREAM_ID, None)
            for table, properties in self.expected_metadata().items()}
        if not stream:
            return parent_stream
        return parent_stream[stream]
