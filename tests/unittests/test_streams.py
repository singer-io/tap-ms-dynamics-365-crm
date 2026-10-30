import unittest
from unittest.mock import MagicMock, patch

from tap_ms_dynamics_365_crm.streams.streams import (
    get_streams,
    call_entity_definitions,
    build_entity_metadata,
    build_schema,
)
from tap_ms_dynamics_365_crm.streams.abstracts import BaseStream
from tap_ms_dynamics_365_crm.client import (
    AUTH_METHOD_AUTHORIZATION_CODE,
    AUTH_METHOD_CLIENT_CREDENTIALS,
)
from tap_ms_dynamics_365_crm.exceptions import MSDynamics365CrmForbiddenError
from tap_ms_dynamics_365_crm.streams import CLIENT_CREDENTIALS_ONLY_STREAMS, INCLUDED_ENTITIES


class TestMetadataAccessErrors(unittest.TestCase):
    def test_metadata_forbidden_logs_actionable_error_and_preserves_cause(self):
        for endpoint in ('EntityDefinitions', '$metadata'):
            with self.subTest(endpoint=endpoint):
                client = MagicMock()
                original = MSDynamics365CrmForbiddenError(
                    "HTTP-error-code: 403, Error Code: 0x80040220, "
                    "Error: SecLib::CheckPrivilege failed. PrivilegeName: prvReadEntity."
                )
                client.make_request.side_effect = original

                with patch('tap_ms_dynamics_365_crm.streams.streams.LOGGER.error') as log:
                    with self.assertRaises(MSDynamics365CrmForbiddenError) as raised:
                        if endpoint == 'EntityDefinitions':
                            list(call_entity_definitions(client))
                        else:
                            list(build_entity_metadata(client, {}))

                message = str(raised.exception)
                self.assertIn(f"'{endpoint}'", message)
                self.assertIn("Discovery cannot continue", message)
                self.assertIn("Dataverse administrator", message)
                self.assertIn("Entity Read privilege", message)
                self.assertIn(str(original), message)
                self.assertIs(raised.exception.__cause__, original)
                log.assert_called_once_with(message)
                client.make_request.assert_called_once()

    def test_unrelated_metadata_errors_propagate_unchanged(self):
        client = MagicMock()
        original = ValueError("Invalid metadata response")
        client.make_request.side_effect = original

        with patch('tap_ms_dynamics_365_crm.streams.streams.LOGGER.error') as log:
            with self.assertRaises(ValueError) as raised:
                list(build_entity_metadata(client, {}))

        self.assertIs(raised.exception, original)
        log.assert_not_called()


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

    @patch.object(BaseStream, 'check_access', autospec=True, return_value=True)
    @patch('tap_ms_dynamics_365_crm.streams.streams.build_entity_metadata')
    @patch('tap_ms_dynamics_365_crm.streams.streams.flatten_entity_attributes')
    def test_guid_error_streams_require_client_credentials(
        self, mock_flatten, mock_build_entity_metadata, mock_check_access
    ):
        self.assertEqual(len(CLIENT_CREDENTIALS_ONLY_STREAMS), 466)
        self.assertEqual(
            INCLUDED_ENTITIES["client_credentials_entities"],
            CLIENT_CREDENTIALS_ONLY_STREAMS,
        )
        mock_build_entity_metadata.return_value = [
            self._entity(name) for name in sorted(CLIENT_CREDENTIALS_ONLY_STREAMS)
        ]
        mock_flatten.return_value = {'modifiedon': {'type': 'Edm.DateTimeOffset'}}
        for auth_method in (AUTH_METHOD_AUTHORIZATION_CODE, AUTH_METHOD_CLIENT_CREDENTIALS):
            for create_schema in (True, False):
                with self.subTest(auth_method=auth_method, create_schema=create_schema):
                    client = MagicMock(max_pagesize=5000, auth_method=auth_method)
                    client.config = {}
                    streams = get_streams(client, create_schema=create_schema)
                    self.assertEqual(
                        set(streams),
                        CLIENT_CREDENTIALS_ONLY_STREAMS
                        if auth_method == AUTH_METHOD_CLIENT_CREDENTIALS else set(),
                    )
        self.assertEqual(mock_check_access.call_count, 466)

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
        client.auth_method = AUTH_METHOD_AUTHORIZATION_CODE
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
        client.auth_method = AUTH_METHOD_AUTHORIZATION_CODE

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
        client.auth_method = AUTH_METHOD_AUTHORIZATION_CODE

        with self.assertRaises(MSDynamics365CrmForbiddenError):
            get_streams(client, create_schema=True)

    @patch.object(BaseStream, 'check_access', autospec=True, return_value=True)
    @patch('tap_ms_dynamics_365_crm.streams.streams.build_entity_metadata')
    @patch('tap_ms_dynamics_365_crm.streams.streams.flatten_entity_attributes')
    def test_aaduser_is_only_available_with_authorization_code(
        self, mock_flatten, mock_build_entity_metadata, mock_check_access
    ):
        mock_build_entity_metadata.return_value = [self._entity('aaduser')]
        mock_flatten.return_value = {'modifiedon': {'type': 'Edm.DateTimeOffset'}}

        for auth_method, expected in (
            (AUTH_METHOD_AUTHORIZATION_CODE, True),
            (AUTH_METHOD_CLIENT_CREDENTIALS, False),
        ):
            for create_schema in (True, False):
                client = MagicMock()
                client.max_pagesize = 5000
                client.config = {}
                client.auth_method = auth_method

                streams = get_streams(client, create_schema=create_schema)

                self.assertEqual('aaduser' in streams, expected)

        self.assertEqual(mock_check_access.call_count, 1)

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
                "$select": (
                    "MetadataId,LogicalName,EntitySetName,IsCustomEntity,IsManaged,"
                    "PrimaryIdAttribute"
                ),
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

    @patch('tap_ms_dynamics_365_crm.streams.streams.transform_metadata_xml')
    @patch('tap_ms_dynamics_365_crm.streams.streams.call_entity_definitions')
    def test_primary_id_attribute_overrides_xml_key(
        self, mock_call_entity_definitions, mock_transform_metadata_xml
    ):
        """EntityDefinitions' PrimaryIdAttribute (e.g. 'systemuserid' for
        systemuser) is authoritative and must override whatever Key the
        $metadata XML parse produced."""
        mock_call_entity_definitions.return_value = [
            {"LogicalName": "systemuser", "IsCustomEntity": False, "IsManaged": True,
             "EntitySetName": "systemusers", "PrimaryIdAttribute": "systemuserid"},
        ]
        mock_transform_metadata_xml.return_value = {
            "systemuser": {"Key": "ownerid"},
        }

        client = MagicMock()
        included_entities = {"org_core_metadata": {"systemuser"}}

        results = list(build_entity_metadata(client, included_entities))

        self.assertEqual(results[0]["Key"], "systemuserid")

    @patch('tap_ms_dynamics_365_crm.streams.streams.transform_metadata_xml')
    @patch('tap_ms_dynamics_365_crm.streams.streams.call_entity_definitions')
    def test_xml_key_used_when_primary_id_attribute_missing(
        self, mock_call_entity_definitions, mock_transform_metadata_xml
    ):
        """Falls back to the $metadata XML's Key if EntityDefinitions doesn't
        return a PrimaryIdAttribute for some reason."""
        mock_call_entity_definitions.return_value = [
            {"LogicalName": "account", "IsCustomEntity": False, "IsManaged": True,
             "EntitySetName": "accounts"},
        ]
        mock_transform_metadata_xml.return_value = {
            "account": {"Key": "accountid"},
        }

        client = MagicMock()
        included_entities = {"sales": {"account"}}

        results = list(build_entity_metadata(client, included_entities))

        self.assertEqual(results[0]["Key"], "accountid")


class TestGetStreamsInheritedReplicationKey(unittest.TestCase):
    """Regression test: entities that only declare `modifiedon` on a `BaseType`
    (e.g. activity types inheriting from `activitypointer`) must still be built
    as INCREMENTAL streams, not FULL_TABLE, once inherited properties are
    resolved from the real `$metadata` XML."""

    METADATA_XML = '''<?xml version="1.0" encoding="utf-8"?>
    <edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
        <edmx:DataServices>
            <Schema Namespace="Microsoft.Dynamics.CRM" xmlns="http://docs.oasis-open.org/odata/ns/edm">
                <EntityType Name="activitypointer">
                    <Key>
                        <PropertyRef Name="activityid"/>
                    </Key>
                    <Property Name="activityid" Type="Edm.Guid"/>
                    <Property Name="subject" Type="Edm.String"/>
                    <Property Name="modifiedon" Type="Edm.DateTimeOffset"/>
                </EntityType>
                <EntityType Name="email" BaseType="Microsoft.Dynamics.CRM.activitypointer">
                    <Key>
                        <PropertyRef Name="activityid"/>
                    </Key>
                    <Property Name="activityid" Type="Edm.Guid"/>
                    <Property Name="torecipients" Type="Edm.String"/>
                </EntityType>
            </Schema>
        </edmx:DataServices>
    </edmx:Edmx>'''

    @patch('tap_ms_dynamics_365_crm.streams.streams.call_entity_definitions')
    def test_derived_activity_entity_uses_incremental_replication(self, mock_call_entity_definitions):
        mock_call_entity_definitions.return_value = [
            {"LogicalName": "email", "IsCustomEntity": False, "IsManaged": True,
             "EntitySetName": "emails"},
        ]

        client = MagicMock()
        client.make_request.return_value = self.METADATA_XML
        client.max_pagesize = 5000
        client.config = {}

        included_entities = {"field_service": {"email"}}
        with patch('tap_ms_dynamics_365_crm.streams.INCLUDED_ENTITIES', included_entities), \
             patch('tap_ms_dynamics_365_crm.streams.EXCLUDED_ENTITIES', set()):
            streams = get_streams(client, create_schema=False)

        self.assertIn("email", streams)
        self.assertEqual(streams["email"].replication_method, "INCREMENTAL")
        self.assertEqual(streams["email"].replication_keys, ["modifiedon"])


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
