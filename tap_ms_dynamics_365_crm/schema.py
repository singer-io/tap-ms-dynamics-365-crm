import os
import json
import singer
from typing import Dict, Tuple
from singer import metadata
from tap_ms_dynamics_365_crm.client import Client
from tap_ms_dynamics_365_crm.streams import get_streams

LOGGER = singer.get_logger()


def get_schemas(client: Client) -> Tuple[Dict, Dict]:
    """
    Load the schema references, prepare metadata for each streams and return schema and metadata for the catalog.
    """
    schemas = {}
    field_metadata = {}

    streams = get_streams(client)
    LOGGER.info('There are {:d} valid streams in MS Dynamics'.format(len(streams)))

    for stream_name, stream_obj in streams.items():
        schema = stream_obj.schema
        schemas[stream_name] = schema

        mdata = metadata.new()
        mdata = metadata.get_standard_metadata(
            schema=schema,
            key_properties=getattr(stream_obj, "key_properties"),
            valid_replication_keys=(getattr(stream_obj, "valid_replication_keys") or []),
            replication_method=getattr(stream_obj, "replication_method"),
        )
        mdata = metadata.to_map(mdata)

        automatic_keys = getattr(stream_obj, "valid_replication_keys") or []
        for field_name in schema.get("properties", {}).keys():
            if field_name in automatic_keys:
                mdata = metadata.write(
                    mdata, ("properties", field_name), "inclusion", "automatic"
                )

        parent_tap_stream_id = getattr(stream_obj, "parent", None)
        if parent_tap_stream_id:
            mdata = metadata.write(mdata, (), 'parent-tap-stream-id', parent_tap_stream_id)

        if getattr(stream_obj, "module", None):
            mdata = metadata.write(mdata, (), 'module', getattr(stream_obj, "module"))

        mdata = metadata.to_list(mdata)
        field_metadata[stream_name] = mdata

    return schemas, field_metadata
