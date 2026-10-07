import unittest
from unittest.mock import MagicMock, patch

from tap_ms_dynamics_365_crm.streams.streams import (
    get_streams,
    call_entity_definitions,
    build_entity_metadata,
    build_schema,
)
from tap_ms_dynamics_365_crm.streams.abstracts import BaseStream
from tap_ms_dynamics_365_crm.exceptions import MSDynamics365CrmForbiddenError


class TestGetStreamsAccessFiltering(unittest.TestCase):
    """Test that get_streams excludes inaccessible entities from the catalog
    when create_schema=True (discovery), and skips the check during sync."""

    def _entity(self, name, key='id'):
        return {
            "LogicalName": name,
            "EntitySetName": f"{name}s",
            "Key": key,
            "Properties": {},
        }

    @patch.object(BaseStream, 'check_access', autospec=True)
    @patch('tap_ms_dynamics_365_crm.streams.streams.build_entity_metadata')
    @patch('tap_ms_dynamics_365_crm.streams.streams.flatten_entity_attributes')
    def test_inaccessible_stream_excluded_during_discovery(
        self, mock_flatten, mock_build_entity_metadata, mock_check_access
    ):
        mock_build_entity_metadata.return_value = [
            self._entity('aaduser'),
            self._entity('account'),
        ]
        mock_flatten.return_value = {'modifiedon': {'type': 'Edm.DateTimeOffset'}}
        mock_check_access.side_effect = lambda stream_self: stream_self.tap_stream_id != 'aaduser'

        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {}
        streams = get_streams(client, create_schema=True)

        self.assertNotIn('aaduser', streams)
        self.assertIn('account', streams)
        self.assertEqual(mock_check_access.call_count, 2)

    @patch.object(BaseStream, 'check_access', autospec=True)
    @patch('tap_ms_dynamics_365_crm.streams.streams.build_entity_metadata')
    @patch('tap_ms_dynamics_365_crm.streams.streams.flatten_entity_attributes')
    def test_check_access_not_called_when_create_schema_false(
        self, mock_flatten, mock_build_entity_metadata, mock_check_access
    ):
        mock_build_entity_metadata.return_value = [self._entity('account')]
        mock_flatten.return_value = {'modifiedon': {'type': 'Edm.DateTimeOffset'}}

        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {}
        streams = get_streams(client, create_schema=False)

        self.assertIn('account', streams)
        mock_check_access.assert_not_called()

    @patch.object(BaseStream, 'check_access', autospec=True)
    @patch('tap_ms_dynamics_365_crm.streams.streams.build_entity_metadata')
    @patch('tap_ms_dynamics_365_crm.streams.streams.flatten_entity_attributes')
    def test_inaccessible_streams_logged_together_as_one_summary(
        self, mock_flatten, mock_build_entity_metadata, mock_check_access
    ):
        """All inaccessible stream names are collected and logged in a single
        summary warning, rather than only being logged individually."""
        mock_build_entity_metadata.return_value = [
            self._entity('aaduser'),
            self._entity('gitbranch'),
            self._entity('account'),
        ]
        mock_flatten.return_value = {'modifiedon': {'type': 'Edm.DateTimeOffset'}}
        mock_check_access.side_effect = (
            lambda stream_self: stream_self.tap_stream_id not in ('aaduser', 'gitbranch')
        )

        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {}

        with self.assertLogs('root', level='WARNING') as log:
            streams = get_streams(client, create_schema=True)

        self.assertNotIn('aaduser', streams)
        self.assertNotIn('gitbranch', streams)
        self.assertIn('account', streams)
        summary_logs = [msg for msg in log.output if 'aaduser' in msg and 'gitbranch' in msg]
        self.assertEqual(
            len(summary_logs), 1,
            "Expected exactly one summary log line naming all inaccessible streams",
        )

    @patch.object(BaseStream, 'check_access', autospec=True, return_value=False)
    @patch('tap_ms_dynamics_365_crm.streams.streams.build_entity_metadata')
    @patch('tap_ms_dynamics_365_crm.streams.streams.flatten_entity_attributes')
    def test_raises_forbidden_when_all_streams_inaccessible(
        self, mock_flatten, mock_build_entity_metadata, mock_check_access
    ):
        """When every discovered stream is excluded, get_streams raises Forbidden
        rather than silently returning an empty catalog."""
        mock_build_entity_metadata.return_value = [self._entity('aaduser')]
        mock_flatten.return_value = {'modifiedon': {'type': 'Edm.DateTimeOffset'}}

        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {}

        with self.assertRaises(MSDynamics365CrmForbiddenError):
            get_streams(client, create_schema=True)

    @patch('tap_ms_dynamics_365_crm.streams.streams.build_entity_metadata')
    @patch('tap_ms_dynamics_365_crm.streams.streams.flatten_entity_attributes')
    def test_stream_without_name_is_skipped(self, mock_flatten, mock_build_entity_metadata):
        """Entities with no LogicalName are skipped without raising."""
        mock_build_entity_metadata.return_value = [
            {"LogicalName": None, "EntitySetName": "", "Key": "id", "Properties": {}},
            self._entity('account'),
        ]
        mock_flatten.return_value = {'modifiedon': {'type': 'Edm.DateTimeOffset'}}

        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {}
        streams = get_streams(client, create_schema=False)

        self.assertEqual(list(streams.keys()), ['account'])

    @patch('tap_ms_dynamics_365_crm.streams.streams.build_entity_metadata')
    @patch('tap_ms_dynamics_365_crm.streams.streams.flatten_entity_attributes')
    def test_stream_without_modifiedon_uses_full_table_replication(
        self, mock_flatten, mock_build_entity_metadata
    ):
        """Entities lacking a `modifiedon` attribute are built as FULL_TABLE streams."""
        mock_build_entity_metadata.return_value = [self._entity('competitor')]
        mock_flatten.return_value = {'name': {'type': 'Edm.String'}}

        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {}
        streams = get_streams(client, create_schema=False)

        self.assertEqual(streams['competitor'].replication_method, 'FULL_TABLE')

    @patch('tap_ms_dynamics_365_crm.streams.streams.build_entity_metadata')
    @patch('tap_ms_dynamics_365_crm.streams.streams.flatten_entity_attributes')
    def test_stream_with_no_schema_properties_is_skipped_during_discovery(
        self, mock_flatten, mock_build_entity_metadata
    ):
        """Entities whose attributes produce no usable schema properties (e.g.
        only complex/unsupported typed fields) are excluded during discovery."""
        mock_build_entity_metadata.return_value = [
            self._entity('componentversion'),
            self._entity('account'),
        ]
        mock_flatten.side_effect = [
            {'somebinary': {'type': 'Edm.Binary'}},
            {'modifiedon': {'type': 'Edm.DateTimeOffset'}},
        ]

        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {}
        with patch.object(BaseStream, 'check_access', autospec=True, return_value=True):
            streams = get_streams(client, create_schema=True)

        self.assertNotIn('componentversion', streams)
        self.assertIn('account', streams)


class TestCallEntityDefinitions(unittest.TestCase):
    """Test call_entity_definitions"""

    def test_yields_entities_from_response(self):
        client = MagicMock()
        client.make_request.return_value = {
            "@odata.count": 2,
            "value": [{"LogicalName": "account"}, {"LogicalName": "contact"}],
        }

        entities = list(call_entity_definitions(client))

        self.assertEqual(len(entities), 2)
        self.assertEqual(entities[0]["LogicalName"], "account")
        client.make_request.assert_called_once_with(
            method='GET',
            params={
                "$select": "MetadataId,LogicalName,EntitySetName,IsCustomEntity,IsManaged",
                "$count": "true",
            },
            path='EntityDefinitions',
        )


class TestBuildEntityMetadata(unittest.TestCase):
    """Test build_entity_metadata"""

    @patch('tap_ms_dynamics_365_crm.streams.streams.transform_metadata_xml')
    @patch('tap_ms_dynamics_365_crm.streams.streams.call_entity_definitions')
    def test_yields_custom_and_included_entities_present_in_metadata(
        self, mock_call_entity_definitions, mock_transform_metadata_xml
    ):
        mock_call_entity_definitions.return_value = [
            {"LogicalName": "new_customentity", "IsCustomEntity": True, "IsManaged": False,
             "EntitySetName": "new_customentities"},
            {"LogicalName": "account", "IsCustomEntity": False, "IsManaged": True,
             "EntitySetName": "accounts"},
            {"LogicalName": "not_in_metadata", "IsCustomEntity": True, "IsManaged": False,
             "EntitySetName": "not_in_metadatas"},
            {"LogicalName": "contact", "IsCustomEntity": False, "IsManaged": True,
             "EntitySetName": "contacts"},
        ]
        mock_transform_metadata_xml.return_value = {
            "new_customentity": {},
            "account": {},
            "contact": {},
        }

        client = MagicMock()
        included_entities = {"sales": {"account"}}

        results = list(build_entity_metadata(client, included_entities))
        result_names = [r["LogicalName"] for r in results]

        self.assertIn("new_customentity", result_names)
        self.assertIn("account", result_names)
        self.assertNotIn("not_in_metadata", result_names)
        self.assertNotIn("contact", result_names)


class TestBuildSchema(unittest.TestCase):
    """Test build_schema's type mapping for each Dynamics EDM type family"""

    def test_maps_integer_type(self):
        schema = build_schema({'count': {'type': 'Edm.Int32'}})
        self.assertEqual(schema['properties']['count']['type'], ['null', 'integer'])

    def test_maps_number_type(self):
        schema = build_schema({'amount': {'type': 'Edm.Decimal'}})
        self.assertEqual(schema['properties']['amount']['type'], ['null', 'number'])

    def test_maps_boolean_type(self):
        schema = build_schema({'is_active': {'type': 'Edm.Boolean'}})
        self.assertEqual(schema['properties']['is_active']['type'], ['null', 'boolean'])

    def test_skips_complex_type(self):
        schema = build_schema({'blob': {'type': 'Edm.Binary'}})
        self.assertNotIn('blob', schema['properties'])

    def test_maps_date_type_with_format(self):
        schema = build_schema({'modifiedon': {'type': 'Edm.DateTimeOffset'}})
        self.assertEqual(schema['properties']['modifiedon']['type'], ['null', 'string'])
        self.assertEqual(schema['properties']['modifiedon']['format'], 'date-time')
