import singer
from typing import Dict
from tap_ms_dynamics_365_crm.client import Client
from tap_ms_dynamics_365_crm.streams import get_streams


LOGGER = singer.get_logger()


def update_currently_syncing(state: Dict, stream_name: str) -> None:
    """
    Update currently_syncing in state and write it
    """
    if not stream_name and singer.get_currently_syncing(state):
        del state["currently_syncing"]
    else:
        singer.set_currently_syncing(state, stream_name)
    singer.write_state(state)


def get_stream_object(streams: dict, catalog: singer.Catalog, stream_name: str):
    """
    get stream object for stream name and enrich it with catalog metadata
    """
    stream = streams.get(stream_name)
    stream_catalog_entry = catalog.get_stream(stream_name)
    stream_metadata = singer.metadata.to_map(stream_catalog_entry.metadata)
    stream_schema = stream_catalog_entry.schema.to_dict()
    stream.catalog = stream_catalog_entry
    stream.schema = stream_schema
    stream.metadata = stream_metadata

    return stream


def write_schema(stream, client, streams_to_sync, catalog, streams) -> None:
    """
    Write schema for stream and its children
    """
    if stream.is_selected():
        stream.write_schema()

    for child in stream.children:
        child_obj = get_stream_object(streams, catalog, child)
        write_schema(child_obj, client, streams_to_sync, catalog, streams)
        if child in streams_to_sync:
            stream.child_to_sync.append(child_obj)


def sync(client: Client, config: Dict, catalog: singer.Catalog, state) -> None:
    """
    Sync selected streams from catalog
    """
    streams = get_streams(client, create_schema=False)
    streams_to_sync = []
    for stream in catalog.get_selected_streams(state):
        streams_to_sync.append(stream.stream)
    LOGGER.info("selected_streams: {}".format(streams_to_sync))

    last_stream = singer.get_currently_syncing(state)
    LOGGER.info("last/currently syncing stream: {}".format(last_stream))

    with singer.Transformer() as transformer:
        for stream_name in streams_to_sync:
            stream = get_stream_object(streams, catalog, stream_name)
            if stream.parent:
                if stream.parent not in streams_to_sync:
                    streams_to_sync.append(stream.parent)
                continue

            write_schema(stream, client, streams_to_sync, catalog, streams)
            LOGGER.info("START Syncing: {}".format(stream_name))
            update_currently_syncing(state, stream_name)
            total_records = stream.sync(state=state, transformer=transformer)

            update_currently_syncing(state, None)
            LOGGER.info(
                "FINISHED Syncing: {}, total_records: {}".format(
                    stream_name, total_records
                )
            )
