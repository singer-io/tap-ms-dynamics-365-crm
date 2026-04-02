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
        """Exclude streams that have no records in the API response,
           as they will not have any fields to replicate."""
        include_streams = set({
            'account',
            'contact',
            'contracttemplate',
            'entitlemententityallocationtypemapping',
            'incident',
            'knowledgearticle',
            'lead',
            'msdyn_actual',
            'msdyn_bookingsetupmetadata',
            'msdyn_fieldservicesetting',
            'msdyn_fieldserviceslaconfiguration',
            'msdyn_geofencingsettings',
            'msdyn_geolocationsettings',
            'msdyn_priority',
            'msdyn_requirementstatus',
            'msdyn_scheduleboardsetting',
            'msdyn_timeentrysetting',
            'msdyn_warehouse',
            'opportunity',
            'phonetocaseprocess',
            'pricelevel',
            'product',
            'queue',
            'queuemembership',
        })
        # Exclude streams that have no records in the API response
        streams_to_exclude = set(MSDynamics365CRMBaseTest.expected_metadata().keys()).difference(
            include_streams
        )
        return self.expected_stream_names().difference(streams_to_exclude)
