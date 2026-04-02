import unittest

from base import MSDynamics365CRMBaseTest
from parameterized import parameterized_class
from tap_tester.base_suite_tests.start_date_test import StartDateTest


DEFAULT_START_DATE_1 = "2015-03-25T00:00:00Z"
DEFAULT_START_DATE_2 = "2017-01-25T00:00:00Z"

# Optional: override dates per stream.
# Example:
# PER_STREAM_START_DATES = {
#     "account": {
#         "start_date_1": "2015-01-01T00:00:00Z",
#         "start_date_2": "2019-01-01T00:00:00Z",
#     },
# }

PER_STREAM_START_DATES = {
    "account": {
        "start_date_1": "2026-01-01T00:00:00.000000Z",
        "start_date_2": "2026-01-06T14:16:40.000000Z",
    },
    "contact": {
        "start_date_1": "2026-01-01T00:00:00.000000Z",
        "start_date_2": "2026-01-06T14:14:26.000000Z",
    },
    "incident": {
        "start_date_1": "2026-01-01T00:00:00.000000Z",
        "start_date_2": "2026-01-06T14:16:14.000000Z",
    },
    "knowledgearticle": {
        "start_date_1": "2026-01-01T00:00:00.000000Z",
        "start_date_2": "2026-01-06T14:13:12.000000Z",
    },
    "lead": {
        "start_date_1": "2026-01-01T00:00:00.000000Z",
        "start_date_2": "2026-01-06T14:13:46.000000Z",
    },
    "msdyn_bookingsetupmetadata": {
        "start_date_1": "2025-11-01T00:00:00.000000Z",
        "start_date_2": "2025-11-23T20:49:25.000000Z",
    },
    "opportunity": {
        "start_date_1": "2026-01-01T00:00:00.000000Z",
        "start_date_2": "2026-01-06T14:15:10.000000Z",
    },
    "phonetocaseprocess": {
        "start_date_1": "2026-01-01T00:00:00.000000Z",
        "start_date_2": "2026-01-06T14:16:15.000000Z",
    },
    "product": {
        "start_date_1": "2025-12-01T00:00:00.000000Z",
        "start_date_2": "2026-01-06T14:16:35.000000Z",
    },
    "queue": {
        "start_date_1": "2025-11-01T00:00:00.000000Z",
        "start_date_2": "2025-12-06T00:51:36.000000Z",
    }
}

# Include only these streams for start_date testing.
INCLUDED_STREAMS = {
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
}
STREAMS_TO_EXCLUDE = set(MSDynamics365CRMBaseTest.expected_metadata().keys()).difference(
    INCLUDED_STREAMS
)


def _stream_start_date_params():
    """Create one test class per stream with stream-specific start dates."""
    streams = sorted(
        set(MSDynamics365CRMBaseTest.expected_metadata().keys()).difference(STREAMS_TO_EXCLUDE)
    )
    params = []
    for stream in streams:
        stream_dates = PER_STREAM_START_DATES.get(stream, {})
        start_date_1 = stream_dates.get("start_date_1", DEFAULT_START_DATE_1)
        start_date_2 = stream_dates.get("start_date_2", DEFAULT_START_DATE_2)
        params.append((stream, start_date_1, start_date_2))

    return params


@parameterized_class(
    ("test_stream", "start_date_1_value", "start_date_2_value"),
    _stream_start_date_params(),
)
class MSDynamics365CRMStartDateTest(StartDateTest, MSDynamics365CRMBaseTest):
    """Instantiate stream-specific start dates and run start-date tests per stream."""

    @classmethod
    def name(cls):
        return f"tap_tester_ms-dynamics-365-crm_start_date_test_{cls.test_stream}"

    @classmethod
    def setUpClass(cls):
        # Parameterized template class can be collected by unittest; skip it.
        if cls.__name__ == "MSDynamics365CRMStartDateTest":
            raise unittest.SkipTest("Template class; run generated parameterized classes only")

        # Reset shared StartDateTest cache for each generated stream class.
        StartDateTest.record_count_by_stream_1 = None
        StartDateTest.synced_messages_by_stream_1 = None
        StartDateTest.record_count_by_stream_2 = None
        StartDateTest.synced_messages_by_stream_2 = None
        super().setUpClass()

    def streams_to_test(self):
        return {self.test_stream}

    def get_properties(self, original: bool = True):
        """Configuration of properties required for the tap."""
        return {
            "start_date": self.start_date,
            "page_size": 100
        }

    @property
    def start_date_1(self):
        return self.start_date_1_value

    @property
    def start_date_2(self):
        return self.start_date_2_value
