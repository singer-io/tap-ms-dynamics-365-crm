import unittest

from tap_ms_dynamics_365_crm.field_naming import normalize_field_name


class TestNormalizeFieldName(unittest.TestCase):
    """Test normalize_field_name's Precog-compatible renaming rules."""

    def test_plain_attribute_is_unchanged(self):
        self.assertEqual(normalize_field_name('territorycode'), 'territorycode')

    def test_strips_leading_underscore_from_lookup_value(self):
        self.assertEqual(normalize_field_name('_ownerid_value'), 'ownerid_value')

    def test_normalizes_formatted_value_annotation(self):
        self.assertEqual(
            normalize_field_name('territorycode@OData.Community.Display.V1.FormattedValue'),
            'territorycode_odata_community_display_v1_formatted_value',
        )

    def test_normalizes_lookup_annotation_and_strips_prefix(self):
        self.assertEqual(
            normalize_field_name('_ownerid_value@Microsoft.Dynamics.CRM.lookuplogicalname'),
            'ownerid_value_microsoft_dynamics_crm_lookuplogicalname',
        )

    def test_normalizes_navigation_property_annotation_and_strips_prefix(self):
        self.assertEqual(
            normalize_field_name(
                '_ownerid_value@Microsoft.Dynamics.CRM.associatednavigationproperty'
            ),
            'ownerid_value_microsoft_dynamics_crm_associatednavigationproperty',
        )
