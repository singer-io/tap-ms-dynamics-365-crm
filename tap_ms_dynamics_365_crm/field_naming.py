import re

# Dataverse's Web API adds a response-time quirk to raw field names:
# requesting `Prefer: odata.include-annotations="*"` (see
# streams/abstracts.py:ANNOTATIONS_PREFER) adds sibling `@`-suffixed
# annotation properties (e.g. `@OData.Community.Display.V1.FormattedValue`,
# `@Microsoft.Dynamics.CRM.lookuplogicalname`; see
# streams/streams.py:build_annotation_properties()).
#
# That `@...` suffix is awkward for downstream consumers (e.g. destination
# column names), so this module rewrites it to a lowercase, underscore-
# separated form -- generically (every `.` becomes `_`, and a camelCase
# word boundary -- a lowercase letter/digit immediately followed by an
# uppercase letter, e.g. the "dV" in "FormattedValue" -- also becomes `_`),
# rather than matching a fixed list of known suffixes, so any annotation
# Dataverse adds in the future is handled the same way without requiring a
# code change here. Consecutive capitals (e.g. "OData", "CRM") are treated
# as a single acronym and not split. This keeps schema property names
# (streams.py) and raw record keys (streams/abstracts.py) in lockstep.
#
# NOTE: lookup-style attributes (Lookup/Customer/Owner/PartyList) are
# returned by Dataverse as `_<name>_value`, prefixed with an underscore.
# The leading `_` is only stripped on annotation properties
# (e.g. `_ownerid_value@...` -> `ownerid_value_...`): those are
# new fields no existing customer could already have selected, so renaming
# them is safe. The base attribute itself (e.g. `_ownerid_value`) already
# existed before this feature and may already be selected on existing
# catalogs, so its leading `_` is left as-is.
#
# Any `.` in the base attribute name (before `@`) is also replaced with `_`
# -- not just in the annotation suffix -- so the result is always a safe,
# dot-free destination column name regardless of where the `.` appears.
_CAMEL_CASE_BOUNDARY = re.compile(r'(?<=[a-z0-9])(?=[A-Z])')


def normalize_field_name(field_name: str) -> str:
    """Normalizes a raw Dataverse attribute/annotation name.

    Replaces any `.` in the base attribute name with `_`. If a `@...`
    annotation suffix is present, it's additionally rewritten to a
    lowercase, underscore-separated form (inserting `_` at each `.` and at
    each camelCase word boundary, then lowercasing), and -- only in that
    case -- a leading `_` (the lookup-value prefix) is also stripped. A
    plain attribute name with no annotation suffix and no `.` (the vast
    majority, including the leading `_` on lookup-style attributes) is
    returned unchanged.
    """
    base_name, separator, suffix = field_name.partition('@')
    if not separator:
        return base_name.replace('.', '_')

    base_name = base_name.replace('.', '_')
    snake_suffix = _CAMEL_CASE_BOUNDARY.sub('_', suffix).lower().replace('.', '_')
    field_name = f'{base_name}_{snake_suffix}'

    if field_name.startswith('_'):
        field_name = field_name[1:]

    return field_name
