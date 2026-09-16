
from base import MSDynamics365CRMBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest


class MSDynamics365CRMInterruptedSyncTest(InterruptedSyncTest, MSDynamics365CRMBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""

    # Dynamics 365 populates these geocoding fields asynchronously (via a
    # background Bing Maps lookup) some time after a record is created or
    # updated, without necessarily bumping the record's `modifiedon` value.
    # Comparing them across two syncs run a few minutes apart can therefore
    # produce false-positive diffs unrelated to the tap's own behavior, so we
    # exclude them from the strict record-equality check in
    # test_resuming_sync_records.
    VOLATILE_FIELDS = {
        "address1_latitude",
        "address1_longitude",
        "address1_utcoffset",
        "address2_latitude",
        "address2_longitude",
        "address2_utcoffset",
    }

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

    def _strip_volatile_fields(self, records):
        """Return copies of records with known-volatile, asynchronously
        populated fields removed so they don't cause false-positive
        equality failures."""
        return [
            {k: v for k, v in record.items() if k not in self.VOLATILE_FIELDS}
            for record in records
        ]

    def test_resuming_sync_records(self):
        """Verify for all streams that the recovery sync gets all the
        expected records.

        This overrides the base implementation to strip volatile
        geocoding fields (populated asynchronously by Dynamics 365) from
        the compared records, since those fields can change between the
        first and resuming sync calls without indicating a real tap bug.
        """
        incremental_streams = {s for s, m in self.expected_replication_method().items()
                               if m == self.INCREMENTAL}
        currently_syncing_stream = self.manipulate_state()['currently_syncing']
        for stream in self.streams_to_test().intersection(incremental_streams):
            with self.subTest(stream=stream):

                # gather expectations and results
                expected_replication_key = self.expected_replication_keys(stream)
                # Make sure this is not a compound replication key
                assert len(expected_replication_key) == 1
                expected_replication_key = next(iter(expected_replication_key))

                first_sync_records = [
                    record['data'] for record in
                    self.first_sync_records.get(stream, {}).get('messages', [])
                    if record.get('action') == 'upsert']
                resuming_sync_records = [
                    record['data'] for record in
                    self.resuming_sync_records.get(stream, {}).get('messages', [])
                    if record.get('action') == 'upsert']

                stream_bookmark = self.get_bookmark_value(
                    self.manipulate_state(), stream)
                if stream_bookmark:
                    completed = stream != currently_syncing_stream
                    expected_resuming_sync_start_time = self.calculate_expected_sync_start_time(
                        stream_bookmark, stream, completed=completed)
                else:
                    # For not yet started streams there will be no bookmark and we should
                    # sync all records the from the beginning of the original sync.
                    expected_resuming_sync_start_time = min(
                        self.parse_date(record.get(expected_replication_key))
                        for record in first_sync_records)

                # Verify the interrupted sync replicates the expected record set
                # All interrupted recs are in full recs
                # Record count for all streams of interrupted sync match expectations
                first_sync_records_after_bookmark = [
                    record for record in first_sync_records
                    if self.parse_date(record[expected_replication_key]) >=
                    expected_resuming_sync_start_time]
                # remove any records that got added after the first sync
                filtered_resuming_records = [
                    record for record in resuming_sync_records
                    if self.parse_date(record[expected_replication_key]) <=
                    self.parse_date(self.get_bookmark_value(self.first_sync_state, stream))]

                self.assertEqual(
                    self._strip_volatile_fields(first_sync_records_after_bookmark),
                    self._strip_volatile_fields(filtered_resuming_records),
                    msg="Incorrect data in the interrupted sync")
