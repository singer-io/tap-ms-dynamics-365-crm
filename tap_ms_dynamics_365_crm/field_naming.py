# Dataverse's Web API exposes two response-time quirks in raw field names:
#  1. Lookup-style attributes (Lookup/Customer/Owner/PartyList) are returned
#     as `_<name>_value`, prefixed with an underscore.
#  2. Requesting `Prefer: odata.include-annotations="*"` (see
#     streams/abstracts.py:ANNOTATIONS_PREFER) adds sibling `@`-suffixed
#     annotation properties (see streams/streams.py:build_annotation_properties()).
#
# Both are awkward for downstream consumers (e.g. destination column names),
# so this module normalizes them to the lowercase, underscore-separated,
# unprefixed form used by Stitch's Precog connector for the same entities,
# keeping schema property names (streams.py) and raw record keys
# (streams/abstracts.py) in lockstep.
ANNOTATION_SUFFIX_NORMALIZATION = {
    '@OData.Community.Display.V1.FormattedValue': '_odata_community_display_v1_formatted_value',
    '@Microsoft.Dynamics.CRM.lookuplogicalname': '_microsoft_dynamics_crm_lookuplogicalname',
    '@Microsoft.Dynamics.CRM.associatednavigationproperty': '_microsoft_dynamics_crm_associatednavigationproperty',
}


def normalize_field_name(field_name: str) -> str:
    """Normalizes a raw Dataverse attribute/annotation name to its
    Precog-compatible form.

    Rewrites a known `@...` annotation suffix (if present) to its lowercase,
    underscore-separated equivalent, then strips a single leading `_`
    (the lookup-value prefix). Names with neither trait (the vast majority
    of plain attributes) are returned unchanged.
    """
    for suffix, normalized_suffix in ANNOTATION_SUFFIX_NORMALIZATION.items():
        if field_name.endswith(suffix):
            field_name = field_name[:-len(suffix)] + normalized_suffix
            break

    if field_name.startswith('_'):
        field_name = field_name[1:]

    return field_name
