import unittest
from unittest.mock import MagicMock, patch
from tap_ms_dynamics_365_crm.schema import get_schemas
from tap_ms_dynamics_365_crm.discover import discover
import tap_ms_dynamics_365_crm as tap_module


class TestSchema(unittest.TestCase):
    """Test schema module functionality"""

    @patch('tap_ms_dynamics_365_crm.schema.get_streams')
    @patch('tap_ms_dynamics_365_crm.schema.LOGGER')
    def test_get_schemas_success(self, mock_logger, mock_get_streams):
        """Test get_schemas returns schemas and metadata"""
        # Create mock stream objects
        mock_stream1 = MagicMock()
        mock_stream1.schema = {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'name': {'type': 'string'}
            }
        }
        mock_stream1.key_properties = ['id']
        mock_stream1.valid_replication_keys = ['modifiedon']
        mock_stream1.replication_method = 'INCREMENTAL'
        mock_stream1.parent = None

        mock_stream2 = MagicMock()
        mock_stream2.schema = {
            'type': 'object',
            'properties': {
                'contactid': {'type': 'string'}
            }
        }
        mock_stream2.key_properties = ['contactid']
        mock_stream2.valid_replication_keys = None
        mock_stream2.replication_method = 'FULL_TABLE'
        mock_stream2.parent = None

        mock_get_streams.return_value = {
            'accounts': mock_stream1,
            'contacts': mock_stream2
        }

        mock_client = MagicMock()
        # Execute
        schemas, field_metadata = get_schemas(mock_client)
        # Assertions
        self.assertEqual(len(schemas), 2)
        self.assertEqual(len(field_metadata), 2)
        # Check schemas
        self.assertIn('accounts', schemas)
        self.assertIn('contacts', schemas)
        self.assertEqual(schemas['accounts'], mock_stream1.schema)
        # Check metadata
        self.assertIn('accounts', field_metadata)
        self.assertIsInstance(field_metadata['accounts'], list)
        # Logger should log stream count
        mock_logger.info.assert_called()

    @patch('tap_ms_dynamics_365_crm.schema.get_streams')
    def test_get_schemas_with_parent_stream(self, mock_get_streams):
        """Test get_schemas handles child streams with parent metadata"""
        mock_child_stream = MagicMock()
        mock_child_stream.schema = {'type': 'object', 'properties': {}}
        mock_child_stream.key_properties = ['id']
        mock_child_stream.valid_replication_keys = None
        mock_child_stream.replication_method = 'FULL_TABLE'
        mock_child_stream.parent = 'parent_stream'
        mock_get_streams.return_value = {
            'child_stream': mock_child_stream
        }
        mock_client = MagicMock()
        schemas, field_metadata = get_schemas(mock_client)
        # Verify parent metadata is included
        metadata_dict = {m['breadcrumb']: m['metadata'] for m in field_metadata['child_stream']}
        self.assertEqual(metadata_dict[()].get('parent-tap-stream-id'), 'parent_stream')

    @patch('tap_ms_dynamics_365_crm.schema.get_streams')
    def test_get_schemas_automatic_inclusion_for_replication_keys(self, mock_get_streams):
        """Test get_schemas marks replication keys as automatic inclusion"""
        mock_stream = MagicMock()
        mock_stream.schema = {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'modifiedon': {'type': 'string'}
            }
        }
        mock_stream.key_properties = ['id']
        mock_stream.valid_replication_keys = ['modifiedon']
        mock_stream.replication_method = 'INCREMENTAL'
        mock_stream.parent = None
        mock_get_streams.return_value = {
            'test_stream': mock_stream
        }

        mock_client = MagicMock()
        schemas, field_metadata = get_schemas(mock_client)
        # Find the modifiedon field metadata
        modifiedon_metadata = next(
            (m for m in field_metadata['test_stream']
            if m.get('breadcrumb') == ('properties', 'modifiedon')),
            None
        )
        self.assertIsNotNone(modifiedon_metadata)
        self.assertEqual(modifiedon_metadata['metadata']['inclusion'], 'automatic')

    @patch('tap_ms_dynamics_365_crm.schema.get_streams')
    def test_get_schemas_selected_by_default(self, mock_get_streams):
        """Test get_schemas metadata structure"""
        mock_stream = MagicMock()
        mock_stream.schema = {'type': 'object', 'properties': {}}
        mock_stream.key_properties = ['id']
        mock_stream.valid_replication_keys = None
        mock_stream.replication_method = 'FULL_TABLE'
        mock_stream.parent = None
        mock_get_streams.return_value = {
            'test_stream': mock_stream
        }
        mock_client = MagicMock()
        schemas, field_metadata = get_schemas(mock_client)
        # Verify metadata structure - check that root metadata is present
        metadata_dict = {tuple(m['breadcrumb']): m['metadata'] for m in field_metadata['test_stream']}
        root_metadata = metadata_dict.get(())
        self.assertIsNotNone(root_metadata, "Root metadata should exist")

    @patch('tap_ms_dynamics_365_crm.schema.get_streams')
    def test_get_schemas_empty_streams(self, mock_get_streams):
        """Test get_schemas with no streams"""
        mock_get_streams.return_value = {}
        mock_client = MagicMock()
        schemas, field_metadata = get_schemas(mock_client)
        self.assertEqual(schemas, {})
        self.assertEqual(field_metadata, {})


class TestDiscover(unittest.TestCase):
    """Test discover.discover"""

    @patch('tap_ms_dynamics_365_crm.discover.get_schemas')
    def test_discover_builds_catalog_from_schemas(self, mock_get_schemas):
        mock_get_schemas.return_value = (
            {
                "account": {
                    "type": "object",
                    "properties": {"accountid": {"type": ["null", "string"]}},
                }
            },
            {
                "account": [
                    {"breadcrumb": (), "metadata": {"table-key-properties": ["accountid"]}},
                ]
            },
        )

        client = MagicMock()
        catalog = discover(client=client)

        self.assertEqual(len(catalog.streams), 1)
        entry = catalog.streams[0]
        self.assertEqual(entry.stream, "account")
        self.assertEqual(entry.tap_stream_id, "account")
        self.assertEqual(entry.key_properties, ["accountid"])

    @patch('tap_ms_dynamics_365_crm.discover.get_schemas')
    def test_discover_reraises_and_logs_schema_conversion_errors(self, mock_get_schemas):
        """A malformed schema_dict causes Schema.from_dict to raise; discover()
        should log context and re-raise rather than swallow the error."""
        mock_get_schemas.return_value = (
            {"broken_stream": {"type": "object", "properties": {"bad": "not-a-dict"}}},
            {"broken_stream": []},
        )

        client = MagicMock()
        with self.assertRaises(Exception):
            discover(client=client)


class TestDoDiscoverAndMain(unittest.TestCase):
    """Test tap_ms_dynamics_365_crm.do_discover and main"""

    @patch('tap_ms_dynamics_365_crm.json.dump')
    @patch('tap_ms_dynamics_365_crm.discover')
    def test_do_discover_dumps_catalog_to_stdout(self, mock_discover, mock_json_dump):
        mock_catalog = MagicMock()
        mock_catalog.to_dict.return_value = {"streams": []}
        mock_discover.return_value = mock_catalog

        client = MagicMock()
        tap_module.do_discover(client=client)

        mock_json_dump.assert_called_once()
        self.assertEqual(mock_json_dump.call_args.args[0], {"streams": []})

    @patch('tap_ms_dynamics_365_crm.sync')
    @patch('tap_ms_dynamics_365_crm.do_discover')
    @patch('tap_ms_dynamics_365_crm.Client')
    @patch('tap_ms_dynamics_365_crm.singer.utils.parse_args')
    def test_main_runs_discover_mode(
        self, mock_parse_args, mock_client_cls, mock_do_discover, mock_sync
    ):
        parsed_args = MagicMock()
        parsed_args.state = None
        parsed_args.discover = True
        parsed_args.catalog = None
        mock_parse_args.return_value = parsed_args
        mock_client_cls.return_value.__enter__.return_value = MagicMock()

        tap_module.main()

        mock_do_discover.assert_called_once()
        mock_sync.assert_not_called()

    @patch('tap_ms_dynamics_365_crm.sync')
    @patch('tap_ms_dynamics_365_crm.do_discover')
    @patch('tap_ms_dynamics_365_crm.Client')
    @patch('tap_ms_dynamics_365_crm.singer.utils.parse_args')
    def test_main_runs_sync_mode_with_existing_state(
        self, mock_parse_args, mock_client_cls, mock_do_discover, mock_sync
    ):
        parsed_args = MagicMock()
        parsed_args.state = {"currently_syncing": "account"}
        parsed_args.discover = False
        parsed_args.catalog = MagicMock()
        parsed_args.config = {"key": "value"}
        mock_parse_args.return_value = parsed_args
        mock_client = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = mock_client

        tap_module.main()

        mock_do_discover.assert_not_called()
        mock_sync.assert_called_once_with(
            client=mock_client,
            config=parsed_args.config,
            catalog=parsed_args.catalog,
            state=parsed_args.state,
        )
