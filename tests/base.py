import json
import os

from tap_tester.base_suite_tests.base_case import BaseCase
from tap_tester import menagerie, runner


EXPECTED_METADATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "expected_metadata.json"
)
with open(EXPECTED_METADATA_FILE, encoding="utf-8") as _expected_metadata_file:
    EXPECTED_METADATA_RAW = json.load(_expected_metadata_file)


class MSDynamics365CRMBaseTest(BaseCase):
    """Setup expectations for test sub classes.

    Metadata describing streams. A bunch of shared methods that are used
    in tap-tester tests. Shared tap-specific methods (as needed).
    """
    start_date = "2019-01-01T00:00:00Z"
    PARENT_TAP_STREAM_ID = "parent-tap-stream-id"
    _expected_metadata_cache = None

    # Org-specific custom entities (created ad-hoc in the test sandbox using the
    # default "new_" customization prefix) that are not part of the tap's
    # standard expected metadata. These are always excluded from discovery
    # test comparisons so the test suite doesn't break when the sandbox's
    # custom entities change.
    # "componentversionnrddatasource" is an elastic table that the sandbox
    # intermittently rejects with HTTP 400 0x80097259 ("elastic child unowned
    # table ... without parent record value"). The failures come in bursts
    # lasting longer than the tap's access-check retries, so the stream's
    # presence in the catalog is not deterministic. It is excluded from the
    # comparison regardless of whether discovery returns it.
    CUSTOM_STREAMS_TO_SKIP = {
        "componentversionnrddatasource",
        "new_testcustomactivity",
        "new_testelastic",
        "new_testequipmentlog",
        "new_testproject",
        "new_testrichtype",
        "new_testsurveyresponse",
    }

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

        cls._expected_metadata_cache = {
            stream_name: {
                cls.PRIMARY_KEYS: set(stream_info.get("primary_keys", [])),
                cls.REPLICATION_METHOD: stream_info.get("replication_method", cls.INCREMENTAL),
                cls.REPLICATION_KEYS: set(stream_info.get("replication_keys", [])),
                cls.OBEYS_START_DATE: stream_info.get("obeys_start_date", True),
                cls.API_LIMIT: stream_info.get("api_limit", 100),
            }
            for stream_name, stream_info in EXPECTED_METADATA_RAW.items()
        }

        return cls._expected_metadata_cache

    def run_and_verify_check_mode(self, conn_id):
        """
        Run check mode and verify it succeeds, excluding the org-specific
        custom entities in CUSTOM_STREAMS_TO_SKIP from the discovered catalog
        before comparing against expected streams.

        Return the found catalogs from menagerie.
        """
        check_job_name = runner.run_check_mode(self, conn_id)

        exit_status = menagerie.get_exit_status(conn_id, check_job_name)
        menagerie.verify_check_exit_status(self, exit_status, check_job_name)

        found_catalogs = [
            catalog for catalog in menagerie.get_catalogs(conn_id)
            if catalog['stream_name'] not in self.CUSTOM_STREAMS_TO_SKIP
        ]
        self.assertGreater(len(found_catalogs), 0,
                           logging="A catalog was produced by discovery.")

        found_stream_names = {catalog['stream_name'] for catalog in found_catalogs}
        self.assertSetEqual(self.expected_stream_names(), found_stream_names,
                            logging="Expected streams are present in catalog.")

        return found_catalogs


    @staticmethod
    def get_credentials():
        """Authentication information for the test account."""
        credentials_dict = {}
        creds = {
            'auth_method': 'client_credentials',
            'client_id': 'TAP_MS_DYNAMICS_365_CRM_CLIENT_ID',
            'client_secret': 'TAP_MS_DYNAMICS_365_CRM_CLIENT_SECRET',
            'organization_uri': 'TAP_MS_DYNAMICS_365_CRM_ORGANIZATION_URI',
            'tenant_id': 'TAP_MS_DYNAMICS_365_CRM_TENANT_ID',
            'refresh_token': 'TAP_MS_DYNAMICS_365_CRM_REFRESH_TOKEN',
        }

        for cred in creds:
            if cred == 'auth_method':
                credentials_dict[cred] = creds[cred]
            else:
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
