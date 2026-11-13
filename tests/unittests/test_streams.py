import unittest
from unittest.mock import MagicMock, patch

from tap_ms_dynamics_365_crm.streams.streams import (
    get_streams,
    call_entity_definitions,
    build_entity_metadata,
    build_schema,
    IGNORED_ENTITY_PREFIXES,
)
from tap_ms_dynamics_365_crm.streams.abstracts import BaseStream
from tap_ms_dynamics_365_crm.client import (
    AUTH_METHOD_AUTHORIZATION_CODE,
    AUTH_METHOD_CLIENT_CREDENTIALS,
)
from tap_ms_dynamics_365_crm.exceptions import MSDynamics365CrmForbiddenError


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
                            list(build_entity_metadata(client))

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
                list(build_entity_metadata(client))

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
    @patch('tap_ms_dynamics_365_crm.streams.streams.transform_metadata_xml')
    @patch('tap_ms_dynamics_365_crm.streams.streams.flatten_entity_attributes')
    def test_mserp_virtual_entities_are_never_probed_during_discovery(
        self, mock_flatten, mock_transform_metadata_xml, mock_check_access
    ):
        """F&O / mserp_ tables must be filtered out before any check_access() table

        probe occurs, preventing 401 unauthorized errors during discovery.
        """
        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {}
        client.auth_method = AUTH_METHOD_AUTHORIZATION_CODE

        def mock_make_request(method, path, **kwargs):
            if path == 'EntityDefinitions':
                return {
                    "@odata.count": 2,
                    "value": [
                        {
                            "LogicalName": "mserp_custcustomerv3entity",
                            "EntitySetName": "mserp_custcustomerv3entities",
                            "IsIntersect": False,
                            "PrimaryIdAttribute": "mserp_custcustomerv3entityid",
                        },
                        {
                            "LogicalName": "account",
                            "EntitySetName": "accounts",
                            "IsIntersect": False,
                            "PrimaryIdAttribute": "accountid",
                        },
                    ],
                }
            if path == '$metadata':
                return "<xml />"
            return {}

        client.make_request.side_effect = mock_make_request
        mock_transform_metadata_xml.return_value = {
            "account": {
                "LogicalName": "account",
                "EntitySetName": "accounts",
                "Key": "accountid",
                "Properties": {},
            },
            "mserp_custcustomerv3entity": {
                "LogicalName": "mserp_custcustomerv3entity",
                "EntitySetName": "mserp_custcustomerv3entities",
                "Key": "mserp_custcustomerv3entityid",
                "Properties": {},
            },
        }
        mock_flatten.return_value = {'modifiedon': {'type': 'Edm.DateTimeOffset'}}
        mock_check_access.return_value = True

        streams = get_streams(client, create_schema=True)

        self.assertIn("account", streams)
        self.assertNotIn("mserp_custcustomerv3entity", streams)
        # check_access should only be called once for 'account', NEVER for 'mserp_*'
        self.assertEqual(mock_check_access.call_count, 1)

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
    def test_aaduser_is_available_regardless_of_auth_method(
        self, mock_flatten, mock_build_entity_metadata, mock_check_access
    ):
        """Entity availability is no longer gated by a static auth-method
        allow-list; check_access() is the sole arbiter of inclusion."""
        mock_build_entity_metadata.return_value = [self._entity('aaduser')]
        mock_flatten.return_value = {'modifiedon': {'type': 'Edm.DateTimeOffset'}}

        for auth_method in (AUTH_METHOD_AUTHORIZATION_CODE, AUTH_METHOD_CLIENT_CREDENTIALS):
            for create_schema in (True, False):
                client = MagicMock()
                client.max_pagesize = 5000
                client.config = {}
                client.auth_method = auth_method

                streams = get_streams(client, create_schema=create_schema)

                self.assertIn('aaduser', streams)

        self.assertEqual(mock_check_access.call_count, 2)

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
                    "MetadataId,LogicalName,EntitySetName,IsIntersect,"
                    "PrimaryIdAttribute"
                ),
                "$count": "true",
            },
            path='EntityDefinitions',
        )

    def test_filters_mserp_fno_virtual_entities(self):
        """Entities prefixed with mserp_ (case-insensitive) are skipped and logged at DEBUG."""
        client = MagicMock()
        client.make_request.return_value = {
            "@odata.count": 4,
            "value": [
                {"LogicalName": "account"},
                {"LogicalName": "mserp_custcustomerv3entity"},
                {"LogicalName": "MSERP_salesorderheaderv2entity"},
                {"LogicalName": "contact"},
            ],
        }

        with patch('tap_ms_dynamics_365_crm.streams.streams.LOGGER.debug') as mock_debug:
            entities = list(call_entity_definitions(client))

        logical_names = [e.get("LogicalName") for e in entities]
        self.assertEqual(logical_names, ["account", "contact"])
        self.assertEqual(mock_debug.call_count, 2)
        mock_debug.assert_any_call(
            "Skipping Finance & Operations virtual entity: %s",
            "mserp_custcustomerv3entity",
        )
        mock_debug.assert_any_call(
            "Skipping Finance & Operations virtual entity: %s",
            "MSERP_salesorderheaderv2entity",
        )

    def test_handles_entities_with_missing_or_none_logical_name(self):
        """Entities missing LogicalName or having None do not raise an AttributeError."""
        client = MagicMock()
        client.make_request.return_value = {
            "@odata.count": 2,
            "value": [{"LogicalName": None}, {}],
        }

        entities = list(call_entity_definitions(client))
        self.assertEqual(len(entities), 2)


class TestBuildEntityMetadata(unittest.TestCase):
    """Test build_entity_metadata"""

    @patch('tap_ms_dynamics_365_crm.streams.streams.transform_metadata_xml')
    @patch('tap_ms_dynamics_365_crm.streams.streams.call_entity_definitions')
    def test_yields_entities_present_in_metadata_excluding_intersect(
        self, mock_call_entity_definitions, mock_transform_metadata_xml
    ):
        """Every entity returned by EntityDefinitions and found in $metadata is
        yielded, regardless of custom/managed status, except IsIntersect
        (N:N relationship/junction) entities."""
        mock_call_entity_definitions.return_value = [
            {"LogicalName": "new_customentity", "IsIntersect": False,
             "EntitySetName": "new_customentities"},
            {"LogicalName": "account", "IsIntersect": False,
             "EntitySetName": "accounts"},
            {"LogicalName": "not_in_metadata", "IsIntersect": False,
             "EntitySetName": "not_in_metadatas"},
            {"LogicalName": "contact_relationship", "IsIntersect": True,
             "EntitySetName": "contact_relationshipset"},
        ]
        mock_transform_metadata_xml.return_value = {
            "new_customentity": {},
            "account": {},
            "contact_relationship": {},
        }

        client = MagicMock()

        results = list(build_entity_metadata(client))
        result_names = [r["LogicalName"] for r in results]

        self.assertIn("new_customentity", result_names)
        self.assertIn("account", result_names)
        self.assertNotIn("not_in_metadata", result_names)
        self.assertNotIn("contact_relationship", result_names)

    @patch('tap_ms_dynamics_365_crm.streams.streams.transform_metadata_xml')
    @patch('tap_ms_dynamics_365_crm.streams.streams.call_entity_definitions')
    def test_primary_id_attribute_overrides_xml_key(
        self, mock_call_entity_definitions, mock_transform_metadata_xml
    ):
        """EntityDefinitions' PrimaryIdAttribute (e.g. 'systemuserid' for
        systemuser) is authoritative and must override whatever Key the
        $metadata XML parse produced."""
        mock_call_entity_definitions.return_value = [
            {"LogicalName": "systemuser", "EntitySetName": "systemusers",
             "PrimaryIdAttribute": "systemuserid"},
        ]
        mock_transform_metadata_xml.return_value = {
            "systemuser": {"Key": "ownerid"},
        }

        client = MagicMock()

        results = list(build_entity_metadata(client))

        self.assertEqual(results[0]["Key"], "systemuserid")

    @patch('tap_ms_dynamics_365_crm.streams.streams.transform_metadata_xml')
    @patch('tap_ms_dynamics_365_crm.streams.streams.call_entity_definitions')
    def test_xml_key_used_when_primary_id_attribute_missing(
        self, mock_call_entity_definitions, mock_transform_metadata_xml
    ):
        """Falls back to the $metadata XML's Key if EntityDefinitions doesn't
        return a PrimaryIdAttribute for some reason."""
        mock_call_entity_definitions.return_value = [
            {"LogicalName": "account", "EntitySetName": "accounts"},
        ]
        mock_transform_metadata_xml.return_value = {
            "account": {"Key": "accountid"},
        }

        client = MagicMock()

        results = list(build_entity_metadata(client))

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
            {"LogicalName": "email", "EntitySetName": "emails"},
        ]

        client = MagicMock()
        client.make_request.return_value = self.METADATA_XML
        client.max_pagesize = 5000
        client.config = {}

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
