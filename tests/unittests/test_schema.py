import unittest
from unittest.mock import MagicMock, patch
from tap_ms_dynamics_365_crm.schema import get_schemas


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
        mock_stream1.module = 'sales'

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
        mock_stream2.module = None

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
        mock_child_stream.module = 'sales'
        mock_get_streams.return_value = {
            'child_stream': mock_child_stream
        }
        mock_client = MagicMock()
        schemas, field_metadata = get_schemas(mock_client)
        # Verify parent metadata is included
        metadata_dict = {m['breadcrumb']: m['metadata'] for m in field_metadata['child_stream']}
        self.assertEqual(metadata_dict[()].get('parent-tap-stream-id'), 'parent_stream')

    @patch('tap_ms_dynamics_365_crm.schema.get_streams')
    def test_get_schemas_with_module_metadata(self, mock_get_streams):
        """Test get_schemas includes module in metadata"""
        mock_stream = MagicMock()
        mock_stream.schema = {'type': 'object', 'properties': {}}
        mock_stream.key_properties = ['id']
        mock_stream.valid_replication_keys = None
        mock_stream.replication_method = 'FULL_TABLE'
        mock_stream.parent = None
        mock_stream.module = 'field_service'
        mock_get_streams.return_value = {
            'test_stream': mock_stream
        }
        mock_client = MagicMock()
        schemas, field_metadata = get_schemas(mock_client)
        # Verify module metadata is included
        metadata_dict = {m['breadcrumb']: m['metadata'] for m in field_metadata['test_stream']}
        self.assertEqual(metadata_dict[()].get('module'), 'field_service')

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
        mock_stream.module = None
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
        """Test get_schemas marks streams as selected by default"""
        mock_stream = MagicMock()
        mock_stream.schema = {'type': 'object', 'properties': {}}
        mock_stream.key_properties = ['id']
        mock_stream.valid_replication_keys = None
        mock_stream.replication_method = 'FULL_TABLE'
        mock_stream.parent = None
        mock_stream.module = None
        mock_get_streams.return_value = {
            'test_stream': mock_stream
        }
        mock_client = MagicMock()
        schemas, field_metadata = get_schemas(mock_client)
        # Verify selected metadata
        metadata_dict = {m['breadcrumb']: m['metadata'] for m in field_metadata['test_stream']}
        self.assertEqual(metadata_dict[()].get('selected'), True)

    @patch('tap_ms_dynamics_365_crm.schema.get_streams')
    def test_get_schemas_empty_streams(self, mock_get_streams):
        """Test get_schemas with no streams"""
        mock_get_streams.return_value = {}
        mock_client = MagicMock()
        schemas, field_metadata = get_schemas(mock_client)
        self.assertEqual(schemas, {})
        self.assertEqual(field_metadata, {})
