"""Test that with no fields selected for a stream automatic fields are still
replicated."""
from base import MSDynamics365CRMBaseTest
from tap_tester.base_suite_tests.automatic_fields_test import MinimumSelectionTest


class MSDynamics365CRMAutomaticFields(MinimumSelectionTest, MSDynamics365CRMBaseTest):
    """Test that with no fields selected for a stream automatic fields are
    still replicated."""

    @staticmethod
    def name():
        return "tap_tester_ms_dynamics_365_crm_automatic_fields_test"

    def streams_to_test(self):
        streams_to_exclude = set()
        return self.expected_stream_names().difference(streams_to_exclude)

