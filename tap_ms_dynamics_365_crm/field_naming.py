# Dataverse's Web API adds a response-time quirk to raw field names:
# requesting `Prefer: odata.include-annotations="*"` (see
# streams/abstracts.py:ANNOTATIONS_PREFER) adds sibling `@`-suffixed
# annotation properties (see streams/streams.py:build_annotation_properties()).
#
# That `@...` suffix is awkward for downstream consumers (e.g. destination
# column names), so this module rewrites it to a lowercase, underscore-
# separated form, keeping schema property names (streams.py) and raw record
# keys (streams/abstracts.py) in lockstep.
#
# NOTE: lookup-style attributes (Lookup/Customer/Owner/PartyList) are
# returned by Dataverse as `_<name>_value`, prefixed with an underscore.
# The leading `_` is only stripped on annotation properties
# (e.g. `_ownerid_value@...` -> `ownerid_value_...`): those are
# new fields no existing customer could already have selected, so renaming
# them is safe. The base attribute itself (e.g. `_ownerid_value`) already
# existed before this feature and may already be selected on existing
# catalogs, so its leading `_` is left as-is.
ANNOTATION_SUFFIX_NORMALIZATION = {
    '@OData.Community.Display.V1.FormattedValue': '_odata_community_display_v1_formatted_value',
    '@Microsoft.Dynamics.CRM.lookuplogicalname': '_microsoft_dynamics_crm_lookuplogicalname',
    '@Microsoft.Dynamics.CRM.associatednavigationproperty': '_microsoft_dynamics_crm_associatednavigationproperty',
}


def normalize_field_name(field_name: str) -> str:
    """Normalizes a raw Dataverse attribute/annotation name.

    Rewrites a known `@...` annotation suffix (if present) to its lowercase,
    underscore-separated equivalent, and -- only in that case -- also
    strips a leading `_` (the lookup-value prefix). A plain attribute name
    with no annotation suffix (including the leading `_` on lookup-style
    attributes) is returned unchanged.
    """
    for suffix, normalized_suffix in ANNOTATION_SUFFIX_NORMALIZATION.items():
        if field_name.endswith(suffix):
            field_name = field_name[:-len(suffix)] + normalized_suffix
            if field_name.startswith('_'):
                field_name = field_name[1:]
            break

    return field_name
