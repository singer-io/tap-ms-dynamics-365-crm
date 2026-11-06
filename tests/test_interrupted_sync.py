
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

                self._verify_resuming_records(
                    stream=stream,
                    replication_key=expected_replication_key,
                    first_sync_records=first_sync_records,
                    first_sync_records_after_bookmark=first_sync_records_after_bookmark,
                    resuming_sync_records=resuming_sync_records,
                    filtered_resuming_records=filtered_resuming_records)

    def _verify_resuming_records(self, stream, replication_key, first_sync_records,
                                 first_sync_records_after_bookmark, resuming_sync_records,
                                 filtered_resuming_records):
        """Compare first-sync and resuming-sync records by primary key,
        tolerating records that Dynamics 365 itself modified between the two
        syncs.

        Records can be updated by platform background jobs (for example
        `knowledgearticle` records appear to be re-stamped periodically) while
        the test is running, which bumps `modifiedon`. A strict list equality
        then fails even though the tap behaved correctly, because the resuming
        sync correctly returns the newer version of the record.

        Still verified (so real tap bugs are caught):
          - every first-sync record at/after the expected start time is
            replicated again by the resuming sync (nothing is dropped);
          - a record whose `modifiedon` is unchanged is identical in both syncs
            (ignoring the volatile geocoding fields);
          - the resuming sync does not replicate unknown records, nor records
            older than the expected start time that were not updated upstream.
        """
        primary_key = next(iter(self.expected_primary_keys(stream)))

        first_all_by_pk = {rec[primary_key]: rec for rec in first_sync_records}
        first_after_by_pk = {rec[primary_key]: rec for rec in first_sync_records_after_bookmark}
        resuming_all_by_pk = {rec[primary_key]: rec for rec in resuming_sync_records}
        filtered_resuming_by_pk = {rec[primary_key]: rec for rec in filtered_resuming_records}

        # Nothing may be dropped by the resuming sync
        self.assertSetEqual(
            set(first_after_by_pk) - set(resuming_all_by_pk), set(),
            msg=f"Records from the first sync missing in the resuming sync for {stream}")

        # Nothing unknown may be replicated
        self.assertSetEqual(
            set(filtered_resuming_by_pk) - set(first_all_by_pk), set(),
            msg=f"Resuming sync replicated records unknown to the first sync for {stream}")

        # Records replicated that the first sync did not return at/after the
        # expected start time must have been updated upstream since.
        for pk, resuming_record in filtered_resuming_by_pk.items():
            if pk in first_after_by_pk:
                continue
            self.assertGreater(
                self.parse_date(resuming_record[replication_key]),
                self.parse_date(first_all_by_pk[pk][replication_key]),
                msg=f"Record {pk} in {stream} was replicated before the expected "
                    "resuming start time without having been updated")

        for pk, first_record in first_after_by_pk.items():
            resuming_record = resuming_all_by_pk[pk]
            if (self.parse_date(resuming_record[replication_key]) >
                    self.parse_date(first_record[replication_key])):
                # Updated by Dynamics between the two syncs; the resuming sync
                # correctly returned the newer version.
                continue
            self.assertEqual(
                self._strip_volatile_fields([first_record]),
                self._strip_volatile_fields([resuming_record]),
                msg=f"Incorrect data in the interrupted sync for {stream} record {pk}")
