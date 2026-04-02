import unittest
from unittest.mock import patch, MagicMock
from tap_ms_dynamics_365_crm.sync import write_schema, sync, update_currently_syncing, get_stream_object

class TestSync(unittest.TestCase):

    def _create_mock_catalog(self):
        """Helper to create a mock catalog with standard configuration"""
        catalog = MagicMock()
        catalog_entry = MagicMock()
        catalog_entry.schema.to_dict.return_value = {"type": "object"}
        catalog_entry.metadata = []
        catalog.get_stream.return_value = catalog_entry
        return catalog

    def _create_mock_stream(self, is_selected=True, children=None, parent=None, sync_return=10):
        """Helper to create a mock stream object with common attributes"""
        stream = MagicMock()
        stream.is_selected.return_value = is_selected
        stream.children = children or []
        stream.child_to_sync = []
        stream.parent = parent
        stream.sync.return_value = sync_return
        return stream

    @patch("tap_ms_dynamics_365_crm.sync.singer.metadata.to_map", return_value={})
    def test_write_schema_only_parent_selected(self, mock_to_map):
        mock_stream = self._create_mock_stream(children=["invoice_payments", "invoice_line_items"])
        catalog = self._create_mock_catalog()
        client = MagicMock()
        streams = {
            "invoice_payments": self._create_mock_stream(),
            "invoice_line_items": self._create_mock_stream()
        }

        write_schema(mock_stream, client, [], catalog, streams)

        mock_stream.write_schema.assert_called_once()
        self.assertEqual(len(mock_stream.child_to_sync), 0)

    @patch("tap_ms_dynamics_365_crm.sync.singer.metadata.to_map", return_value={})
    def test_write_schema_parent_child_both_selected(self, mock_to_map):
        mock_stream = self._create_mock_stream(children=["invoice_payments", "invoice_line_items"])
        catalog = self._create_mock_catalog()
        client = MagicMock()
        streams = {
            "invoice_payments": self._create_mock_stream(),
            "invoice_line_items": self._create_mock_stream()
        }

        write_schema(mock_stream, client, ["invoice_payments"], catalog, streams)

        mock_stream.write_schema.assert_called_once()
        self.assertEqual(len(mock_stream.child_to_sync), 1)

    @patch("tap_ms_dynamics_365_crm.sync.singer.metadata.to_map", return_value={})
    def test_write_schema_child_selected(self, mock_to_map):
        mock_stream = self._create_mock_stream(is_selected=False, children=["invoice_payments", "invoice_line_items"])
        catalog = self._create_mock_catalog()
        client = MagicMock()
        streams = {
            "invoice_payments": self._create_mock_stream(),
            "invoice_line_items": self._create_mock_stream()
        }

        write_schema(mock_stream, client, ["invoice_payments", "invoice_line_items"], catalog, streams)

        self.assertEqual(mock_stream.write_schema.call_count, 0)
        self.assertEqual(len(mock_stream.child_to_sync), 2)

    @patch("tap_ms_dynamics_365_crm.sync.singer.metadata.to_map", return_value={"key": "value"})
    def test_get_stream_object(self, mock_to_map):
        """Test get_stream_object enriches stream with catalog metadata"""
        mock_stream = MagicMock()
        streams = {"test_stream": mock_stream}
        catalog = self._create_mock_catalog()
        catalog.get_stream.return_value.metadata = "metadata"

        result = get_stream_object(streams, catalog, "test_stream")

        self.assertEqual(result.catalog, catalog.get_stream.return_value)
        self.assertEqual(result.schema, {"type": "object"})
        self.assertEqual(result.metadata, {"key": "value"})

    @patch("tap_ms_dynamics_365_crm.sync.get_streams")
    @patch("singer.write_schema")
    @patch("singer.get_currently_syncing")
    @patch("singer.Transformer")
    @patch("singer.write_state")
    def test_sync_stream1_called(self, mock_write_state, mock_transformer, 
                                 mock_get_currently_syncing, mock_write_schema, mock_get_streams):
        # Create mock streams
        mock_get_streams.return_value = {
            "invoices": self._create_mock_stream(parent=None),
            "expenses": self._create_mock_stream(parent=None, sync_return=5)
        }

        mock_catalog = MagicMock()
        mock_catalog.get_selected_streams.return_value = [
            MagicMock(stream="invoices"),
            MagicMock(stream="expenses")
        ]
        mock_catalog.get_stream.side_effect = lambda name: MagicMock(
            schema=MagicMock(to_dict=lambda: {}),
            metadata=[]
        )

        sync(MagicMock(), {}, mock_catalog, {})

        # Both streams should be synced
        self.assertEqual(mock_get_streams.return_value["invoices"].sync.call_count, 1)
        self.assertEqual(mock_get_streams.return_value["expenses"].sync.call_count, 1)

    @patch("tap_ms_dynamics_365_crm.sync.get_streams")
    @patch("singer.write_schema")
    @patch("singer.get_currently_syncing")
    @patch("singer.Transformer")
    @patch("singer.write_state")
    def test_sync_child_selected(self, mock_write_state, mock_transformer,
                                 mock_get_currently_syncing, mock_write_schema, mock_get_streams):
        # Create parent and child stream objects
        parent_stream = self._create_mock_stream(parent=None)
        child_stream1 = self._create_mock_stream(parent="parent_stream")
        child_stream2 = self._create_mock_stream(parent="parent_stream")

        mock_get_streams.return_value = {
            "invoice_messages": child_stream1,
            "invoice_payments": child_stream2,
            "parent_stream": parent_stream
        }

        mock_catalog = MagicMock()
        mock_catalog.get_selected_streams.return_value = [
            MagicMock(stream="invoice_messages"),
            MagicMock(stream="invoice_payments")
        ]
        mock_catalog.get_stream.side_effect = lambda name: MagicMock(
            schema=MagicMock(to_dict=lambda: {}),
            metadata=[]
        )

        sync(MagicMock(), {}, mock_catalog, {})

        # Only parent should be synced, not the child streams directly
        self.assertEqual(parent_stream.sync.call_count, 1)
        self.assertEqual(child_stream1.sync.call_count, 0)
        self.assertEqual(child_stream2.sync.call_count, 0)

    @patch("singer.get_currently_syncing")
    @patch("singer.set_currently_syncing")
    @patch("singer.write_state")
    def test_remove_currently_syncing(self, mock_write_state, mock_set_currently_syncing, mock_get_currently_syncing):
        mock_get_currently_syncing.return_value = "some_stream"
        state = {"currently_syncing": "some_stream"}

        update_currently_syncing(state, None)

        mock_get_currently_syncing.assert_called_once_with(state)
        mock_set_currently_syncing.assert_not_called()
        mock_write_state.assert_called_once_with(state)
        self.assertNotIn("currently_syncing", state)

    @patch("singer.get_currently_syncing")
    @patch("singer.set_currently_syncing")
    @patch("singer.write_state")
    def test_set_currently_syncing(self, mock_write_state, mock_set_currently_syncing, mock_get_currently_syncing):
        mock_get_currently_syncing.return_value = None
        state = {}

        update_currently_syncing(state, "new_stream")

        mock_get_currently_syncing.assert_not_called()
        mock_set_currently_syncing.assert_called_once_with(state, "new_stream")
        mock_write_state.assert_called_once_with(state)
        self.assertNotIn("currently_syncing", state)
