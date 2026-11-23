import singer

from tap_ms_dynamics_365_crm.client import Client
from tap_ms_dynamics_365_crm.field_naming import normalize_field_name
from tap_ms_dynamics_365_crm.xml_transformer import (
    flatten_entity_attributes,
    transform_metadata_xml
)
from tap_ms_dynamics_365_crm.streams.abstracts import (
    IncrementalStream,
    FullTableStream
)
from tap_ms_dynamics_365_crm.exceptions import MSDynamics365CrmForbiddenError

LOGGER = singer.get_logger()

# Virtual entities originating from Dynamics 365 Finance & Operations (ERP)
# use the managed prefix 'mserp_'. Probing these tables without F&O service-to-service
# permissions results in HTTP 401 Unauthorized errors during discovery.
IGNORED_ENTITY_PREFIXES = (
    'mserp_',
)

# Per Microsoft's own Dataverse table-reference criteria, a pure N:N
# junction entity (not useful on its own) has at most this many columns --
# just the two relationship ends plus the intersect PK and maybe a name.
# See build_entity_metadata().
PURE_JUNCTION_MAX_ATTRIBUTES = 4

STRING_TYPES = set([
    'Edm.String',
    'Edm.Guid',
])

INTEGER_TYPES = set([
    'Edm.Int32',
    'Edm.Int64',
])

NUMBER_TYPES = set([
    'Edm.Decimal',
    'Edm.Double',
])

DATE_TYPES = set([
    'Edm.DateTimeOffset',
    'Edm.Date',
])

BOOL_TYPES = set(['Edm.Boolean'])

# Edm.Binary backs large blobs (e.g. entityimage, document bodies) that
# aren't useful synced as base64 strings, so attributes of this type are
# omitted from the schema entirely (see build_schema()).
IGNORED_TYPES = set([
    'Edm.Binary',
])

# Dataverse declares `mscrm.BooleanManagedProperty` as a fixed OData
# complex type with exactly these three sub-properties (see
# learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/
# reference/booleanmanagedproperty), so build_schema() maps it to a
# strictly-typed nested object instead of a flat scalar.
MANAGED_PROPERTY_TYPES = set([
    'mscrm.BooleanManagedProperty',
])

# Dataverse `AttributeType` values (from `EntityDefinitions(...)/Attributes`)
# for which the Web API emits an `@OData.Community.Display.V1.FormattedValue`
# annotation when a request sends `Prefer: odata.include-annotations="*"`.
# These annotations never appear in `$metadata` CSDL (they're response-time
# decorations, not declared data-model properties), so they must be
# synthesized from each attribute's semantic type rather than discovered.
LOOKUP_ATTRIBUTE_TYPES = frozenset([
    'Lookup', 'Customer', 'Owner', 'PartyList',
])

FORMATTED_VALUE_ATTRIBUTE_TYPES = LOOKUP_ATTRIBUTE_TYPES | frozenset([
    'Picklist', 'State', 'Status', 'MultiSelectPicklist', 'Money', 'DateTime', 'Boolean',
])

# Dataverse's older `AttributeType` enum reports some column kinds as the
# generic 'Virtual' value instead of their real semantic type; the actual
# type is only available via the newer `AttributeTypeName.Value` property
# (e.g. 'MultiSelectPicklistType'). See
# https://learn.microsoft.com/en-us/power-apps/developer/data-platform/entity-attribute-metadata
# ("Don't be confused by the AttributeType property... Refer to the
# AttributeTypeName property rather than the AttributeType property.").
# Multi-select choice columns are the only 'Virtual'-reported type in
# FORMATTED_VALUE_ATTRIBUTE_TYPES, so only that one needs resolving here.
VIRTUAL_ATTRIBUTE_TYPE = 'Virtual'
MULTISELECT_PICKLIST_ATTRIBUTE_TYPE_NAME = 'MultiSelectPicklistType'

REPLICATION_TO_STREAM_MAP = {
    'INCREMENTAL': IncrementalStream,
    'FULL_TABLE': FullTableStream
}

def _request_metadata(client: Client, path: str, **kwargs):
    try:
        return client.make_request(method='GET', path=path, **kwargs)
    except MSDynamics365CrmForbiddenError as exc:
        message = (
            f"HTTP-error-code: 403, Error: Cannot read Dataverse metadata from "
            f"'{path}'. Discovery cannot continue without metadata access. "
            "Ask your Dataverse administrator to grant the authenticated user "
            "or application user a security role with the required metadata "
            "Read privileges. If the original error names 'prvReadEntity', "
            "grant the Entity Read privilege. "
            f"Original error: {exc}"
        )
        LOGGER.error(message)
        raise MSDynamics365CrmForbiddenError(message) from exc


def call_entity_definitions(client: Client):
    """Calls the `EntityDefinitions` endpoint to get all entities, excluding
    Dynamics 365 Finance and Operations (mserp_) virtual entities.
    """
    params = {
        "$select": (
            "MetadataId,LogicalName,EntitySetName,IsIntersect,"
            "PrimaryIdAttribute"
        ),
        # Expanding Attributes here (one request for every entity) lets
        # build_entity_metadata() learn each attribute's semantic
        # AttributeType (e.g. 'Picklist', 'Lookup') in addition to the
        # generic Edm.* type $metadata provides, without an extra
        # per-entity round trip. AttributeTypeName is also requested since
        # AttributeType alone reports some types (e.g. multi-select choice
        # columns) only as the generic 'Virtual' value -- see
        # VIRTUAL_ATTRIBUTE_TYPE above.
        "$expand": "Attributes($select=LogicalName,AttributeType,AttributeTypeName)",
        "$count": "true",
    }

    results = _request_metadata(
        client,
        params=params,
        path='EntityDefinitions'
    )

    LOGGER.info('MS Dynamics returned total {} entities'.format(results.get("@odata.count")))

    for entity in results.get('value', []):
        logical_name = entity.get('LogicalName') or ''
        if logical_name.lower().startswith(IGNORED_ENTITY_PREFIXES):
            LOGGER.debug("Skipping Finance & Operations virtual entity: %s", logical_name)
            continue
        yield entity

def _resolve_attribute_type(attr: dict) -> str:
    """Resolves an attribute's real semantic type, correcting for Dataverse
    reporting some types (e.g. multi-select choice columns) as the generic
    'Virtual' `AttributeType` value. See VIRTUAL_ATTRIBUTE_TYPE above.
    """
    attribute_type = attr.get("AttributeType")
    if attribute_type == VIRTUAL_ATTRIBUTE_TYPE:
        type_name = (attr.get("AttributeTypeName") or {}).get("Value")
        if type_name == MULTISELECT_PICKLIST_ATTRIBUTE_TYPE_NAME:
            return "MultiSelectPicklist"
    return attribute_type

def build_entity_metadata(client: Client):
    """Builds entity metadata from the `$metadata` endpoints.

    Every entity returned by `EntityDefinitions` and present in `$metadata` is
    yielded, except pure N:N junction entities: Microsoft's own criteria for
    a "useful" intersect entity
    (https://learn.microsoft.com/en-us/power-apps/developer/data-platform/reference/about-entity-reference)
    is `IsIntersect` false, or `IsIntersect` true with more than
    `PURE_JUNCTION_MAX_ATTRIBUTES` columns -- most intersect entities only
    have the handful of columns needed to support the relationship and
    carry no other data, but some (e.g. `listmember`, which also tracks
    `entitytype`/`entityid`/audit columns) are real business data.
    Actual read access for the remaining entities is verified later via
    `BaseStream.check_access()`.
    """
    entity_definitions = call_entity_definitions(client)
    metadata = _request_metadata(client, path='$metadata')
    entity_metadata = transform_metadata_xml(metadata)

    for entity in entity_definitions:
        entity_name = entity.get("LogicalName")
        attribute_count = len(entity.get("Attributes") or [])
        is_pure_junction_table = (
            entity.get("IsIntersect") and attribute_count <= PURE_JUNCTION_MAX_ATTRIBUTES
        )
        if is_pure_junction_table or entity_name not in entity_metadata:
            continue
        entity_metadata[entity_name]["LogicalName"] = entity_name
        entity_metadata[entity_name]["EntitySetName"] = entity.get("EntitySetName")
        # EntityDefinitions' PrimaryIdAttribute is the authoritative primary
        # key; fall back to the $metadata XML's <Key> only if it's absent.
        entity_metadata[entity_name]["Key"] = (
            entity.get("PrimaryIdAttribute") or entity_metadata[entity_name].get("Key")
        )
        entity_metadata[entity_name]["AttributeTypes"] = {
            attr.get("LogicalName"): _resolve_attribute_type(attr)
            for attr in entity.get("Attributes") or []
            if attr.get("LogicalName")
        }
        yield entity_metadata[entity_name]

def get_streams(client: Client, create_schema: bool = True) -> dict:
    """Builds stream objects for all entities in MS Dynamics and returns a dict
    of stream_name: stream_obj.

    Args:
        client: MS Dynamics client instance
        create_schema: Flag to control schema creation (default: True)
    """
    from tap_ms_dynamics_365_crm.streams import ENTITY_SET_NAME_OVERRIDES

    STREAMS = {} # pylint: disable=invalid-name
    inaccessible_streams = []
    replication_key = 'modifiedon'

    # dynamically build streams by iterating over entities and calling build_schema()
    for stream in build_entity_metadata(client):
        stream_name = stream.get('LogicalName')
        # Some internal/system entities report an EntitySetName casing that
        # does not match their actual (case-sensitive) registered route.
        stream_endpoint = ENTITY_SET_NAME_OVERRIDES.get(stream_name) or stream.get('EntitySetName') or ''
        stream_key = stream.get('Key')
        LOGGER.info('Processing stream: {}'.format(stream_name))

        # skip over any streams that don't have a name
        if not stream_name:
            continue

        attributes = flatten_entity_attributes(
            stream.get('Properties'), stream.get('AttributeTypes')
        )

        if 'modifiedon' in attributes.keys():
            replication_method = 'INCREMENTAL'
            replication_key = 'modifiedon'
        else:
            replication_method = 'FULL_TABLE'

        stream_class = REPLICATION_TO_STREAM_MAP.get(replication_method)
        stream_obj = stream_class(client)
        stream_obj.tap_stream_id = stream_name
        stream_obj.key_properties = [stream_key]
        stream_obj.path = stream_endpoint
        stream_obj.replication_method = replication_method

        if replication_method == 'INCREMENTAL':
            stream_obj.replication_keys = [replication_key]
            stream_obj.valid_replication_keys = [replication_key]

        if create_schema:
            # build schema and skip over any streams with no valid fields
            stream_obj.schema = build_schema(attributes)
            if not stream_obj.schema.get('properties'):
                continue

            # Add key to the schema if missing
            if stream_obj.key_properties[0] not in stream_obj.schema.get('properties'):
                stream_obj.schema['properties'][stream_obj.key_properties[0]] = {
                    'type': ['null', 'string']
                }

            # verify the credentials can actually read this entity before
            # adding it to the catalog
            if not stream_obj.check_access():
                inaccessible_streams.append(stream_name)
                continue
        else:
            stream_obj.schema = {}

        STREAMS.update({stream_name: stream_obj})

    if create_schema and not STREAMS and inaccessible_streams:
        raise MSDynamics365CrmForbiddenError(
            "HTTP-error-code: 403, Error: The credentials do not have "
            "'read' access to any supported streams."
        )

    if create_schema and inaccessible_streams:
        LOGGER.warning(
            "Unauthorized streams excluded from catalog: %s",
            ", ".join(inaccessible_streams),
        )

    return STREAMS

def build_annotation_properties(attr_name: str, attribute_type: str) -> dict:
    """Synthesizes the OData annotation properties Dataverse adds alongside a
    base attribute when a request sends `Prefer: odata.include-annotations="*"`.

    These annotations (a human-readable formatted value, and for lookups the
    referenced entity's logical name and navigation property) never appear
    as declared `$metadata` properties -- they only exist on the response
    payload -- so they must be derived from the attribute's semantic
    `AttributeType` rather than discovered from the CSDL document.
    """
    if attribute_type not in FORMATTED_VALUE_ATTRIBUTE_TYPES:
        return {}

    # Property names are normalized (see field_naming.py) so they match the
    # record keys get_records() normalizes at sync time.
    annotations = {
        normalize_field_name(f'{attr_name}@OData.Community.Display.V1.FormattedValue'): {
            'type': ['null', 'string']
        }
    }

    if attribute_type in LOOKUP_ATTRIBUTE_TYPES:
        annotations[
            normalize_field_name(f'{attr_name}@Microsoft.Dynamics.CRM.lookuplogicalname')
        ] = {'type': ['null', 'string']}
        annotations[
            normalize_field_name(f'{attr_name}@Microsoft.Dynamics.CRM.associatednavigationproperty')
        ] = {'type': ['null', 'string']}

    return annotations

def build_schema(attributes: dict):
    """Builds JSON schema for a stream based on the entity attributes and their types."""
    json_props = {}

    for attr_name, attr_props in attributes.items():
        dyn_type = attr_props.get('type')

        if dyn_type in IGNORED_TYPES:
            # Backs large blobs (e.g. entityimage, document bodies); not
            # useful synced as base64 strings, so the property is omitted.
            continue

        if dyn_type in MANAGED_PROPERTY_TYPES:
            # Fixed shape per Dataverse's complex type declaration: typing
            # each sub-property lets singer.Transformer validate/coerce
            # them individually instead of passing an opaque blob through.
            prop_json_schema = {
                'type': ['null', 'object'],
                'properties': {
                    'Value': {'type': ['null', 'boolean']},
                    'CanBeChanged': {'type': ['null', 'boolean']},
                    'ManagedPropertyLogicalName': {'type': ['null', 'string']},
                },
                'additionalProperties': False,
            }
        else:
            json_type = 'string'
            json_format = None

            if dyn_type in DATE_TYPES:
                json_format = 'date-time'
            elif dyn_type in INTEGER_TYPES:
                json_type = 'integer'
            elif dyn_type in NUMBER_TYPES:
                json_type = 'number'
            elif dyn_type in BOOL_TYPES:
                json_type = 'boolean'

            prop_json_schema = {
                'type': ['null', json_type]
            }

            if json_format:
                prop_json_schema['format'] = json_format

        # Keeps the base property name in lockstep with get_records()'s
        # normalization (only rewrites an `@...` annotation suffix; plain
        # attribute names, including the lookup `_value` prefix, pass
        # through unchanged -- see field_naming.py).
        json_props[normalize_field_name(attr_name)] = prop_json_schema
        json_props.update(
            build_annotation_properties(attr_name, attr_props.get('attribute_type'))
        )

    schema = {
        'type': 'object',
        'additionalProperties': False,
        'properties': json_props
    }

    return schema
