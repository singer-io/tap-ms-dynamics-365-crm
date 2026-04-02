import unittest

from parameterized import parameterized_class
from tap_tester.base_suite_tests.pagination_test import PaginationTest
from base import MSDynamics365CRMBaseTest


DEFAULT_PAGE_SIZE = 20

PER_STREAM_PAGE_SIZES = {
    "account": 10,
    "contact": 10,
    "lead": 10,
    "opportunity": 10,
    'incident': 25,
    'knowledgearticle': 16,
    'phonetocaseprocess': 22,
    'product': 15,
    'queue': 200,
    'queuemembership': 200
}

INCLUDED_STREAMS = {
    'account',
    'contact',
    'incident',
    'knowledgearticle',
    'lead',
    'opportunity',
    'phonetocaseprocess',
    'product',
    'queue',
    'queuemembership',
}

# Exclude streams that have no records in the API response, as they will not have any pages to paginate through.
STREAMS_TO_EXCLUDE = set(MSDynamics365CRMBaseTest.expected_metadata().keys()).difference(
    INCLUDED_STREAMS
)


def _pagination_params():
    """Create one test class per stream with stream-specific page size."""
    streams = sorted(
        set(MSDynamics365CRMBaseTest.expected_metadata().keys()).difference(STREAMS_TO_EXCLUDE)
    )
    return [
        (stream, PER_STREAM_PAGE_SIZES.get(stream, DEFAULT_PAGE_SIZE))
        for stream in streams
    ]


@parameterized_class(("test_stream", "page_size_value"), _pagination_params())
class MSDynamics365CRMPaginationTest(PaginationTest, MSDynamics365CRMBaseTest):
    """
    Ensure tap can replicate multiple pages of data for streams that use pagination.
    """

    @classmethod
    def name(cls):
        return (
            "tap_tester_ms_dynamics_365_crm_pagination_test_"
            f"{cls.test_stream}_page_size_{cls.page_size_value}"
        )

    @classmethod
    def setUpClass(cls):
        # Parameterized template class can be collected by unittest; skip it.
        if cls.__name__ == "MSDynamics365CRMPaginationTest":
            raise unittest.SkipTest("Template class; run generated parameterized classes only")

        # Reset shared PaginationTest cache for each generated stream class.
        PaginationTest.synced_records = None
        PaginationTest.record_count_by_stream = None

        super().setUpClass()

    def get_properties(self, original: bool = True):
        props = super().get_properties(original=original)
        props["page_size"] = self.page_size_value
        return props

    def streams_to_test(self):
        return {self.test_stream}
