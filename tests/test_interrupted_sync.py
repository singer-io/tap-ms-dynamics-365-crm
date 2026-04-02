
from base import MSDynamics365CRMBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest

# versionnumber is a SQL Server rowversion incremented by Dynamics 365 on every
# backend write (SLA KPI recalculations, audit log, queue processing), independently
# of modifiedon.  In CI the gap between the two sync runs is long enough for these
# background processes to bump the value, causing false record-diff failures.
VOLATILE_FIELDS = {"versionnumber"}


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

    def get_properties(self, original: bool = True):
        """Configuration of properties required for the tap."""
        return {
            "start_date": self.start_date,
            "page_size": 100
        }

    def manipulate_state(self):
        return {
            "currently_syncing": "incident",
            "bookmarks": {
                "account": {"modifiedon": "2026-01-01T00:00:00.000000Z"},
                "contact": {"modifiedon": "2026-01-01T00:00:00.000000Z"},
                "incident": {"modifiedon": "2026-01-05T14:15:44.000000Z"},
            }
        }

    def test_resuming_sync_records(self):
        """
        Override the base test to strip volatile system fields before comparing records.
        versionnumber is a SQL Server rowversion that Dynamics 365 background processes
        (SLA KPI timers, audit log, queue processing) increment independently of modifiedon.
        In CI, the time gap between the two sync runs is large enough for these processes
        to mutate the value, causing false failures even though the tap behaviour is correct.
        """
        incremental_streams = {s for s, m in self.expected_replication_method().items()
                               if m == self.INCREMENTAL}
        currently_syncing_stream = self.manipulate_state()['currently_syncing']
        for stream in self.streams_to_test().intersection(incremental_streams):
            with self.subTest(stream=stream):
                expected_replication_key = self.expected_replication_keys(stream)
                assert len(expected_replication_key) == 1
                expected_replication_key = next(iter(expected_replication_key))

                first_sync_records = [
                    {k: v for k, v in record['data'].items() if k not in VOLATILE_FIELDS}
                    for record in self.first_sync_records.get(stream, {}).get('messages', [])
                    if record.get('action') == 'upsert']
                resuming_sync_records = [
                    {k: v for k, v in record['data'].items() if k not in VOLATILE_FIELDS}
                    for record in self.resuming_sync_records.get(stream, {}).get('messages', [])
                    if record.get('action') == 'upsert']

                stream_bookmark = self.get_bookmark_value(self.manipulate_state(), stream)
                if stream_bookmark:
                    completed = stream != currently_syncing_stream
                    expected_resuming_sync_start_time = self.calculate_expected_sync_start_time(
                        stream_bookmark, stream, completed=completed)
                else:
                    expected_resuming_sync_start_time = min(
                        self.parse_date(record.get(expected_replication_key))
                        for record in first_sync_records)

                first_sync_records_after_bookmark = [
                    record for record in first_sync_records
                    if self.parse_date(record[expected_replication_key]) >=
                    expected_resuming_sync_start_time]
                filtered_resuming_records = [
                    record for record in resuming_sync_records
                    if self.parse_date(record[expected_replication_key]) <=
                    self.parse_date(self.get_bookmark_value(self.first_sync_state, stream))]
                self.assertEqual(first_sync_records_after_bookmark, filtered_resuming_records,
                                 msg="Incorrect data in the interrupted sync")
