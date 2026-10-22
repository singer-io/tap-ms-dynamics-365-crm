import unittest
from tap_ms_dynamics_365_crm.xml_transformer import (
    flatten_entity_attributes,
    transform_metadata_xml,
    NS
)


class TestXmlTransformer(unittest.TestCase):
    """Test XML transformer functionality"""

    def test_flatten_entity_attributes_empty_list(self):
        """Test flatten_entity_attributes with empty list"""
        result = flatten_entity_attributes([])

        self.assertEqual(result, {})

    def test_flatten_entity_attributes_single_attribute(self):
        """Test flatten_entity_attributes with single attribute"""
        attributes = [
            {'LogicalName': 'accountid', 'PropertyType': 'Edm.Guid'}
        ]

        result = flatten_entity_attributes(attributes)
        self.assertEqual(result, {
            'accountid': {'type': 'Edm.Guid'}
        })

    def test_flatten_entity_attributes_multiple_attributes(self):
        """Test flatten_entity_attributes with multiple attributes"""
        attributes = [
            {'LogicalName': 'accountid', 'PropertyType': 'Edm.Guid'},
            {'LogicalName': 'name', 'PropertyType': 'Edm.String'},
            {'LogicalName': 'revenue', 'PropertyType': 'Edm.Decimal'}
        ]

        result = flatten_entity_attributes(attributes)
        self.assertEqual(len(result), 3)
        self.assertEqual(result['accountid'], {'type': 'Edm.Guid'})
        self.assertEqual(result['name'], {'type': 'Edm.String'})
        self.assertEqual(result['revenue'], {'type': 'Edm.Decimal'})

    def test_transform_metadata_xml_simple_entity(self):
        """Test transform_metadata_xml with simple entity"""
        xml = '''<?xml version="1.0" encoding="utf-8"?>
        <edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
            <edmx:DataServices>
                <Schema Namespace="Microsoft.Dynamics.CRM" xmlns="http://docs.oasis-open.org/odata/ns/edm">
                    <EntityType Name="account">
                        <Key>
                            <PropertyRef Name="accountid"/>
                        </Key>
                        <Property Name="accountid" Type="Edm.Guid"/>
                        <Property Name="name" Type="Edm.String"/>
                    </EntityType>
                </Schema>
            </edmx:DataServices>
        </edmx:Edmx>'''

        result = transform_metadata_xml(xml)

        self.assertIn('account', result)
        self.assertEqual(result['account']['Key'], 'accountid')
        self.assertEqual(len(result['account']['Properties']), 2)

        # Check properties
        props = result['account']['Properties']
        prop_names = [p['LogicalName'] for p in props]
        self.assertIn('accountid', prop_names)
        self.assertIn('name', prop_names)

    def test_transform_metadata_xml_multiple_entities(self):
        """Test transform_metadata_xml with multiple entities"""
        xml = '''<?xml version="1.0" encoding="utf-8"?>
        <edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
            <edmx:DataServices>
                <Schema Namespace="Microsoft.Dynamics.CRM" xmlns="http://docs.oasis-open.org/odata/ns/edm">
                    <EntityType Name="account">
                        <Key>
                            <PropertyRef Name="accountid"/>
                        </Key>
                        <Property Name="accountid" Type="Edm.Guid"/>
                    </EntityType>
                    <EntityType Name="contact">
                        <Key>
                            <PropertyRef Name="contactid"/>
                        </Key>
                        <Property Name="contactid" Type="Edm.Guid"/>
                        <Property Name="fullname" Type="Edm.String"/>
                    </EntityType>
                </Schema>
            </edmx:DataServices>
        </edmx:Edmx>'''

        result = transform_metadata_xml(xml)

        self.assertEqual(len(result), 2)
        self.assertIn('account', result)
        self.assertIn('contact', result)
        self.assertEqual(result['account']['Key'], 'accountid')
        self.assertEqual(result['contact']['Key'], 'contactid')

    def test_transform_metadata_xml_entity_without_key(self):
        """Test transform_metadata_xml skips entities without Key"""
        xml = '''<?xml version="1.0" encoding="utf-8"?>
        <edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
            <edmx:DataServices>
                <Schema Namespace="Microsoft.Dynamics.CRM" xmlns="http://docs.oasis-open.org/odata/ns/edm">
                    <EntityType Name="account">
                        <Key>
                            <PropertyRef Name="accountid"/>
                        </Key>
                        <Property Name="accountid" Type="Edm.Guid"/>
                    </EntityType>
                    <EntityType Name="invalid_entity">
                        <Property Name="somefield" Type="Edm.String"/>
                    </EntityType>
                </Schema>
            </edmx:DataServices>
        </edmx:Edmx>'''

        result = transform_metadata_xml(xml)
        # Only account should be included, invalid_entity should be skipped
        self.assertEqual(len(result), 1)
        self.assertIn('account', result)
        self.assertNotIn('invalid_entity', result)

    def test_transform_metadata_xml_empty_entity(self):
        """Test transform_metadata_xml skips empty entities"""
        xml = '''<?xml version="1.0" encoding="utf-8"?>
        <edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
            <edmx:DataServices>
                <Schema Namespace="Microsoft.Dynamics.CRM" xmlns="http://docs.oasis-open.org/odata/ns/edm">
                    <EntityType Name="empty_entity"/>
                    <EntityType Name="account">
                        <Key>
                            <PropertyRef Name="accountid"/>
                        </Key>
                        <Property Name="accountid" Type="Edm.Guid"/>
                    </EntityType>
                </Schema>
            </edmx:DataServices>
        </edmx:Edmx>'''
        result = transform_metadata_xml(xml)
        # Only account should be included
        self.assertEqual(len(result), 1)
        self.assertIn('account', result)
        self.assertNotIn('empty_entity', result)

    def test_transform_metadata_xml_various_property_types(self):
        """Test transform_metadata_xml with various property types"""
        xml = '''<?xml version="1.0" encoding="utf-8"?>
        <edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
            <edmx:DataServices>
                <Schema Namespace="Microsoft.Dynamics.CRM" xmlns="http://docs.oasis-open.org/odata/ns/edm">
                    <EntityType Name="entity">
                        <Key>
                            <PropertyRef Name="id"/>
                        </Key>
                        <Property Name="id" Type="Edm.Guid"/>
                        <Property Name="text_field" Type="Edm.String"/>
                        <Property Name="number_field" Type="Edm.Int32"/>
                        <Property Name="decimal_field" Type="Edm.Decimal"/>
                        <Property Name="date_field" Type="Edm.DateTimeOffset"/>
                        <Property Name="boolean_field" Type="Edm.Boolean"/>
                    </EntityType>
                </Schema>
            </edmx:DataServices>
        </edmx:Edmx>'''
        result = transform_metadata_xml(xml)
        props = result['entity']['Properties']
        self.assertEqual(len(props), 6)
        # Verify all property types are captured
        prop_types = {p['LogicalName']: p['PropertyType'] for p in props}
        self.assertEqual(prop_types['text_field'], 'Edm.String')
        self.assertEqual(prop_types['number_field'], 'Edm.Int32')
        self.assertEqual(prop_types['decimal_field'], 'Edm.Decimal')
        self.assertEqual(prop_types['date_field'], 'Edm.DateTimeOffset')
        self.assertEqual(prop_types['boolean_field'], 'Edm.Boolean')

    def test_transform_metadata_xml_no_entities(self):
        """Test transform_metadata_xml with no entities"""
        xml = '''<?xml version="1.0" encoding="utf-8"?>
        <edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
            <edmx:DataServices>
                <Schema Namespace="Microsoft.Dynamics.CRM" xmlns="http://docs.oasis-open.org/odata/ns/edm">
                </Schema>
            </edmx:DataServices>
        </edmx:Edmx>'''
        result = transform_metadata_xml(xml)
        self.assertEqual(result, {})

    def test_namespace_constants(self):
        """Test that namespace constants are correctly defined"""
        self.assertEqual(NS['edmx'], 'http://docs.oasis-open.org/odata/ns/edmx')
        self.assertEqual(NS['edm'], 'http://docs.oasis-open.org/odata/ns/edm')

    def test_transform_metadata_xml_resolves_inherited_properties_from_base_type(self):
        """Derived activity entity types (e.g. `email`) only declare their own
        properties in `$metadata`, while common fields like `modifiedon` are
        declared on the `BaseType` entity (`activitypointer`). Those inherited
        fields must be merged onto the derived entity so callers (and
        `get_streams`) can see `modifiedon` and select INCREMENTAL replication."""
        xml = '''<?xml version="1.0" encoding="utf-8"?>
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

        result = transform_metadata_xml(xml)

        prop_names = {p['LogicalName'] for p in result['email']['Properties']}
        self.assertIn('torecipients', prop_names, "own property should still be present")
        self.assertIn('modifiedon', prop_names, "inherited property should be merged in")
        self.assertIn('subject', prop_names, "inherited property should be merged in")
        # Own `activityid` declaration should not be duplicated by the inherited one.
        activityid_count = sum(1 for p in result['email']['Properties'] if p['LogicalName'] == 'activityid')
        self.assertEqual(activityid_count, 1)

    def test_transform_metadata_xml_derived_property_overrides_base_property(self):
        """A property explicitly redeclared on the derived entity should win over
        the inherited copy from its `BaseType`, rather than being duplicated."""
        xml = '''<?xml version="1.0" encoding="utf-8"?>
        <edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
            <edmx:DataServices>
                <Schema Namespace="Microsoft.Dynamics.CRM" xmlns="http://docs.oasis-open.org/odata/ns/edm">
                    <EntityType Name="activitypointer">
                        <Key>
                            <PropertyRef Name="activityid"/>
                        </Key>
                        <Property Name="activityid" Type="Edm.Guid"/>
                        <Property Name="modifiedon" Type="Edm.DateTimeOffset"/>
                    </EntityType>
                    <EntityType Name="task" BaseType="Microsoft.Dynamics.CRM.activitypointer">
                        <Key>
                            <PropertyRef Name="activityid"/>
                        </Key>
                        <Property Name="activityid" Type="Edm.Guid"/>
                        <Property Name="modifiedon" Type="Edm.String"/>
                    </EntityType>
                </Schema>
            </edmx:DataServices>
        </edmx:Edmx>'''

        result = transform_metadata_xml(xml)

        modifiedon_props = [p for p in result['task']['Properties'] if p['LogicalName'] == 'modifiedon']
        self.assertEqual(len(modifiedon_props), 1)
        self.assertEqual(modifiedon_props[0]['PropertyType'], 'Edm.String')

    def test_transform_metadata_xml_missing_base_type_entity_does_not_crash(self):
        """If `BaseType` points to an entity that isn't captured (e.g. filtered
        out for lacking its own `Key`), inheritance resolution should skip it
        gracefully instead of raising."""
        xml = '''<?xml version="1.0" encoding="utf-8"?>
        <edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
            <edmx:DataServices>
                <Schema Namespace="Microsoft.Dynamics.CRM" xmlns="http://docs.oasis-open.org/odata/ns/edm">
                    <EntityType Name="orphan_child" BaseType="Microsoft.Dynamics.CRM.missing_base">
                        <Key>
                            <PropertyRef Name="orphan_childid"/>
                        </Key>
                        <Property Name="orphan_childid" Type="Edm.Guid"/>
                    </EntityType>
                </Schema>
            </edmx:DataServices>
        </edmx:Edmx>'''

        result = transform_metadata_xml(xml)

        prop_names = {p['LogicalName'] for p in result['orphan_child']['Properties']}
        self.assertEqual(prop_names, {'orphan_childid'})
