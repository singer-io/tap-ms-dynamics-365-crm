import unittest
from unittest.mock import patch, MagicMock
from tap_ms_dynamics_365_crm.streams.abstracts import IncrementalStream

class ConcreteIncrementalStream(IncrementalStream):
    key_properties = ["id"]
    replication_keys = ["updated_at"]
    replication_method = "INCREMENTAL"
    tap_stream_id = "stream_1"
    schema = {"type": "object"}
    path = "test_entity"

class TestIncrementalSync(unittest.TestCase):
    @patch("tap_ms_dynamics_365_crm.streams.abstracts.metadata.to_map")
    def setUp(self, mock_to_map):
        mock_client = MagicMock()
        mock_client.config = {"start_date": "2024-01-01T00:00:00Z"}
        mock_client.max_pagesize = 5000

        mock_catalog = MagicMock()
        mock_catalog.schema.to_dict.return_value = {"key": "value"}
        mock_catalog.metadata = "mock_metadata"
        mock_to_map.return_value = {"metadata_key": "metadata_value"}

        self.stream = ConcreteIncrementalStream(client=mock_client)
        self.stream.catalog = mock_catalog
        self.stream.metadata = {"metadata_key": "metadata_value"}
        self.stream.child_to_sync = []

    @patch("tap_ms_dynamics_365_crm.streams.abstracts.get_bookmark", return_value=100)
    def test_write_bookmark_with_state(self, mock_get_bookmark):
        state = {'bookmarks': {'stream_1': {'updated_at': 100}}}
        result = self.stream.write_bookmark(state, "stream_1", "updated_at", 200)
        self.assertEqual(result, {'bookmarks': {'stream_1': {'updated_at': 200}}})

    @patch("tap_ms_dynamics_365_crm.streams.abstracts.get_bookmark", return_value=100)
    def test_write_bookmark_without_state(self, mock_get_bookmark):
        state = {}
        result = self.stream.write_bookmark(state, "stream_1", "updated_at", 200)
        self.assertEqual(result, {'bookmarks': {'stream_1': {'updated_at': 200}}})

    @patch("tap_ms_dynamics_365_crm.streams.abstracts.get_bookmark", return_value=300)
    def test_write_bookmark_with_old_value(self, mock_get_bookmark):
        state = {'bookmarks': {'stream_1': {'updated_at': 300}}}
        result = self.stream.write_bookmark(state, "stream_1", "updated_at", 200)
        self.assertEqual(result, {'bookmarks': {'stream_1': {'updated_at': 300}}})

    @patch("tap_ms_dynamics_365_crm.streams.abstracts.get_bookmark")
    def test_get_bookmark(self, mock_get_bookmark):
        """Test get_bookmark retrieves correct bookmark value"""
        mock_get_bookmark.return_value = "2024-01-15T00:00:00Z"
        state = {'bookmarks': {'stream_1': {'updated_at': '2024-01-15T00:00:00Z'}}}

        result = self.stream.get_bookmark(state, "stream_1")
        self.assertEqual(result, "2024-01-15T00:00:00Z")

    def test_update_params(self):
        """Test update_params builds correct OData query parameters"""
        self.stream.update_params(filter_value="2024-01-01T00:00:00Z")

        self.assertIn("$orderby", self.stream.params)
        self.assertIn("$filter", self.stream.params)
        self.assertEqual(self.stream.params["$orderby"], "modifiedon asc")
        self.assertIn("modifiedon ge 2024-01-01T00:00:00Z", self.stream.params["$filter"])

    def test_update_params_without_filter(self):
        """Test update_params without filter value"""
        self.stream.update_params()

        self.assertIn("$orderby", self.stream.params)
        self.assertNotIn("$filter", self.stream.params)

    def test_update_header(self):
        """Test update_header updates headers correctly"""
        self.stream.update_header(Prefer="odata.maxpagesize=100")

        self.assertIn("Prefer", self.stream.headers)
        self.assertEqual(self.stream.headers["Prefer"], "odata.maxpagesize=100")
