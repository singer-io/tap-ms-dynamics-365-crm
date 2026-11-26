import unittest

from tap_ms_dynamics_365_crm.field_naming import normalize_field_name


class TestNormalizeFieldName(unittest.TestCase):
    """Test normalize_field_name's annotation-suffix renaming rules."""

    def test_plain_attribute_is_unchanged(self):
        self.assertEqual(normalize_field_name('territorycode'), 'territorycode')

    def test_leading_underscore_on_base_lookup_value_is_preserved(self):
        """The lookup `_value` prefix is intentionally left as-is on the
        base attribute (an existing field that may already be selected on
        existing catalogs); only annotation properties get it stripped."""
        self.assertEqual(normalize_field_name('_ownerid_value'), '_ownerid_value')

    def test_normalizes_formatted_value_annotation(self):
        self.assertEqual(
            normalize_field_name('territorycode@OData.Community.Display.V1.FormattedValue'),
            'territorycode_odata_community_display_v1_formatted_value',
        )

    def test_normalizes_lookup_annotation_and_strips_prefix(self):
        """Annotation properties are new fields no existing customer could
        already have selected, so the leading `_` is stripped here even
        though it's preserved on the underlying base attribute."""
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

    def test_normalizes_formatted_value_annotation_and_strips_prefix(self):
        self.assertEqual(
            normalize_field_name(
                '_ownerid_value@OData.Community.Display.V1.FormattedValue'
            ),
            'ownerid_value_odata_community_display_v1_formatted_value',
        )

    def test_normalizes_an_unrecognized_annotation_suffix_generically(self):
        """The rule isn't a fixed list of known suffixes: any `@...`
        annotation is split on `.` and camelCase word boundaries, then
        lowercased, so a suffix Dataverse hasn't emitted yet is still
        normalized consistently without requiring a code change."""
        self.assertEqual(
            normalize_field_name('msdyn_newfield@Some.Future.AggregatedTotalValue'),
            'msdyn_newfield_some_future_aggregated_total_value',
        )

    def test_keeps_a_run_of_consecutive_capitals_together_as_one_acronym(self):
        """A camelCase boundary is only inserted before an uppercase letter
        that follows a lowercase letter/digit, so a run of consecutive
        capitals (an acronym, e.g. "OData"/"CRM") is kept together rather
        than split letter-by-letter."""
        self.assertEqual(
            normalize_field_name('msdyn_newfield@Some.ABCAcronym'),
            'msdyn_newfield_some_abcacronym',
        )

    def test_replaces_dot_in_base_attribute_name(self):
        """Any `.` in the base attribute name itself (not just in an
        annotation suffix) is also replaced with `_`, so the result is
        always a safe, dot-free destination column name."""
        self.assertEqual(
            normalize_field_name('some.field'),
            'some_field',
        )

    def test_replaces_dot_in_base_attribute_name_alongside_an_annotation(self):
        self.assertEqual(
            normalize_field_name('some.field@OData.Community.Display.V1.FormattedValue'),
            'some_field_odata_community_display_v1_formatted_value',
        )


