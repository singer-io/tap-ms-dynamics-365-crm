from base import MSDynamics365CRMBaseTest
from tap_tester.base_suite_tests.bookmark_test import BookmarkTest


class MSDynamics365CRMBookmarkTest(BookmarkTest, MSDynamics365CRMBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""
    bookmark_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    initial_bookmarks = {
        "bookmarks": {
            "account": {"modifiedon": "2026-01-06T14:16:38.000000Z"},
            "contact": {"modifiedon": "2026-01-05T22:38:12.000000Z"},
            "incident": {"modifiedon": "2026-01-06T14:15:44.000000Z"},
            "knowledgearticle": {"modifiedon": "2026-01-06T14:12:46.000000Z"},
            "lead": {"modifiedon": "2026-01-06T14:13:31.000000Z"},
            "msdyn_bookingsetupmetadata": {"modifiedon": "2025-11-23T20:49:23.000000Z"},
            "opportunity": {"modifiedon": "2026-01-06T14:14:47.000000Z"},
            "phonetocaseprocess": {"modifiedon": "2026-01-06T14:15:46.000000Z"},
            "product": {"modifiedon": "2025-12-05T15:20:10.000000Z"},
            "queue": {"modifiedon": "2025-11-20T05:30:57.000000Z"},
        }
    }

    @staticmethod
    def name():
        return "tap_tester_ms_dynamics_365_crm_bookmark_test"

    def streams_to_test(self):
        included_streams = set({
            "account",
            "contact",
            "incident",
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
