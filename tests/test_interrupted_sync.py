
from base import MSDynamics365CRMBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest


class MSDynamics365CRMInterruptedSyncTest(InterruptedSyncTest, MSDynamics365CRMBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""

    @staticmethod
    def name():
        return "tap_tester_ms_dynamics_365_crm_interrupted_sync_test"

    def streams_to_test(self):
        included_streams = set({
            "account",
            "contact",
            "knowledgearticle",
            "lead",
            "msdyn_bookingsetupmetadata",
            "opportunity",
            "phonetocaseprocess",
            "product",
            "queue",
        })
        streams_to_exclude = set(MSDynamics365CRMBaseTest.expected_metadata().keys()).difference(
            included_streams
        )
        return self.expected_stream_names().difference(streams_to_exclude)

    def get_properties(self, original: bool = True):
        """Configuration of properties required for the tap."""
        return {
            "start_date": self.start_date,
            "page_size": 100
        }

    def manipulate_state(self):
        return {
            "currently_syncing": "contact",
            "bookmarks": {
                "account": {"modifiedon": "2026-01-01T00:00:00.000000Z"},
                "contact": {"modifiedon": "2026-01-01T00:00:00.000000Z"},
            }
        }
