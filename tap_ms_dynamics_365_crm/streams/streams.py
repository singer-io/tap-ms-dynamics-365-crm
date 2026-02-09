import singer

from tap_ms_dynamics_365_crm.client import Client
from tap_ms_dynamics_365_crm.xml_transformer import (
    flatten_entity_attributes,
    transform_metadata_xml
)
from tap_ms_dynamics_365_crm.streams.abstracts import (
    IncrementalStream,
    FullTableStream
)

LOGGER = singer.get_logger()

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

COMPLEX_TYPES = set([
    'Edm.Binary',
    'mscrm.BooleanManagedProperty',
])

REPLICATION_TO_STREAM_MAP = {
    'INCREMENTAL': IncrementalStream,
    'FULL_TABLE': FullTableStream
}

def call_entity_definitions(client: Client):
    """Calls the `EntityDefinitions` endpoint to get all entities."""
    params = {
        "$select": "MetadataId,LogicalName,EntitySetName",
        "$count": "true",
    }

    results = client.make_request(
        method='GET',
        params=params,
        path='EntityDefinitions'
    )

    LOGGER.info('MS Dynamics returned total {} entities'.format(results.get("@odata.count")))

    yield from results.get('value')

def build_entity_metadata(client: Client, included_entities: dict):
    """Builds entity metadata from the `$metadata` endpoints."""
    entity_definitions = call_entity_definitions(client)
    metadata = client.make_request(method='GET', path='$metadata')
    entity_metadata = transform_metadata_xml(metadata)

    for entity in entity_definitions:
        entity_name = entity.get("LogicalName")
        if any(entity_name in entities for entities in included_entities.values()) and entity_name in entity_metadata:
            # checks that entity is in $metadata response
            entity_metadata[entity_name]["LogicalName"] = entity_name
            entity_metadata[entity_name]["EntitySetName"] = entity.get("EntitySetName")

            # Determine module name by checking which module set contains this entity
            module_name = None
            for module, entities in included_entities.items():
                if entity_name in entities:
                    module_name = module
                    break
            entity_metadata[entity_name]["module_name"] = module_name
            yield entity_metadata[entity_name]

def get_streams(client: Client, included_entities: dict = None, excluded_entities: set = None) -> dict:
    """Builds stream objects for all entities in MS Dynamics and returns a dict
    of stream_name: stream_obj."""
    if included_entities is None or excluded_entities is None:
        from tap_ms_dynamics_365_crm.streams import INCLUDED_ENTITIES, EXCLUDED_ENTITIES
        included_entities = included_entities or INCLUDED_ENTITIES
        excluded_entities = excluded_entities or EXCLUDED_ENTITIES

    STREAMS = {} # pylint: disable=invalid-name

    # dynamically build streams by iterating over entities and calling build_schema()
    for stream in build_entity_metadata(client, included_entities):
        stream_name = stream.get('LogicalName')
        stream_endpoint = stream.get('EntitySetName')
        stream_key = stream.get('Key')
        module_name = stream.get('module_name')
        LOGGER.info('Processing stream: {}'.format(stream_name))

        # skip over any streams that don't have a name or are in EXCLUDED_ENTITIES
        if not stream_name or stream_name in excluded_entities:
            continue

        attributes = flatten_entity_attributes(stream.get('Properties'))

        if 'modifiedon' in attributes.keys():
            replication_method = 'INCREMENTAL'
            replication_key = 'modifiedon'
        else:
            replication_method = 'FULL_TABLE'

        stream_class = REPLICATION_TO_STREAM_MAP.get(replication_method)
        stream_obj = stream_class(client)
        stream_obj.tap_stream_id = stream_name
        stream_obj.key_properties = [stream_key]
        stream_obj.url_endpoint = stream_endpoint
        stream_obj.replication_method = replication_method
        stream_obj.module = module_name

        if replication_method == 'INCREMENTAL':
            stream_obj.replication_key = replication_key
            stream_obj.valid_replication_keys = ['modifiedon']

        # build schema and skip over any streams with no valid fields
        stream_obj.schema = build_schema(attributes)
        if not stream_obj.schema.get('properties'):
            continue

        # Add key to the schema if missing
        if stream_obj.key_properties[0] not in stream_obj.schema.get('properties'):
            stream_obj.schema['properties'][stream_obj.key_properties[0]] = {
                'type': ['null', 'string']
            }

        STREAMS.update({stream_name: stream_obj})

    return STREAMS

def build_schema(attributes: dict):
    """Builds JSON schema for a stream based on the entity attributes and their types."""
    json_props = {}

    for attr_name, attr_props in attributes.items():
        dyn_type = attr_props.get('type')
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
        elif dyn_type in COMPLEX_TYPES:
            # TODO: mark as "inclusion": "unsupported"
            continue

        prop_json_schema = {
            'type': ['null', json_type]
        }

        if json_format:
            prop_json_schema['format'] = json_format

        json_props[attr_name] = prop_json_schema

    schema = {
        'type': 'object',
        'additionalProperties': False,
        'properties': json_props
    }

    return schema
