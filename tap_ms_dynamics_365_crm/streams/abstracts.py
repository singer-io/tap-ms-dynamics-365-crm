from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator
from singer import (
    Transformer,
    get_bookmark,
    get_logger,
    metrics,
    write_bookmark,
    write_record,
    write_schema,
    metadata
)
from tap_ms_dynamics_365_crm.client import Client, MAX_PAGESIZE

LOGGER = get_logger()


class BaseStream(ABC):
    """
    A Base Class providing structure and boilerplate for generic streams
    and required attributes for any kind of stream
    ~~~
    Provides:
     - Basic Attributes (stream_name,replication_method,key_properties)
     - Helper methods for catalog generation
     - `sync` and `get_records` method for performing sync
    """

    url_endpoint = ""
    path = ""
    page_size = 100
    parent = ""
    data_key = "value"
    parent_bookmark_key = ""
    http_method = "GET"

    def __init__(self, client: Client = None) -> None:
        self.client = client

        self.child_to_sync = []
        self.tap_stream_id = None
        self.replication_method = None
        self.replication_keys = []
        self.key_properties = []
        self.valid_replication_keys = []
        self.children = []
        self.params = {}
        self.catalog = None
        self.metadata = {}
        self.schema = {}
        self.headers = {'Accept': 'application/json'}
        self.bookmark_value = None

        self.max_pagesize = self.client.max_pagesize if self.client else MAX_PAGESIZE
        configured_page_size = None

        if self.client and getattr(self.client, "config", None):
            configured_page_size = self.client.config.get("page_size")

        if configured_page_size is not None:
            self.page_size = int(configured_page_size)

        self.page_size = self.page_size if self.page_size <= self.max_pagesize else self.max_pagesize

    def is_selected(self):
        if self.catalog:
            return metadata.get(self.metadata, (), "selected")
        return True

    @abstractmethod
    def sync(
        self,
        state: Dict,
        transformer: Transformer,
        parent_obj: Dict = None,
    ) -> Dict:
        """
        Performs a replication sync for the stream.
        ~~~
        Args:
         - state (dict): represents the state file for the tap.
         - transformer (object): A Object of the singer.transformer class.
         - parent_obj (dict): The parent object for the stream.

        Returns:
         - bool: The return value. True for success, False otherwise.

        Docs:
         - https://github.com/singer-io/getting-started/blob/master/docs/SYNC_MODE.md
        """


    def get_records(self) -> Iterator:
        """Interacts with api client interaction and pagination."""
        next_page = True
        endpoint = self.url_endpoint

        while next_page:
            response = self.client.make_request(self.http_method, endpoint, headers=self.headers, params=self.params)

            if '@odata.nextLink' in response:
                endpoint = response.get('@odata.nextLink')
                self.params = {}
            else:
                next_page = False

            yield from response.get(self.data_key, [])

    def write_schema(self) -> None:
        """
        Write a schema message.
        """
        try:
            write_schema(self.tap_stream_id, self.schema, self.key_properties)
        except OSError as err:
            LOGGER.error(
                "OS Error while writing schema for: {}".format(self.tap_stream_id)
            )
            raise err

    def update_header(self, **kwargs) -> None:
        """
        Update headers for the stream
        """
        self.headers.update(kwargs)

    def update_params(self, orderby_key: str = 'modifiedon',
                      replication_key: str = 'modifiedon',
                      filter_value: str = None,
                      secondary_orderby_key: str = None) -> None:
        """
        Build and update OData query parameters for the stream
        """
        orderby_parts = [f'{orderby_key} asc']
        # Secondary sort is appended only when it differs from the primary key.
        # This ensures a stable, deterministic page order when multiple records share
        # the same primary sort value (e.g. two records modified at the same millisecond).
        # Without a tiebreaker, the MS Dynamics OData paging cursor ($skiptoken) can return
        # duplicate or skipped records across pages.
        if secondary_orderby_key and secondary_orderby_key != orderby_key:
            orderby_parts.append(f'{secondary_orderby_key} asc')

        orderby_param = ', '.join(orderby_parts)

        if filter_value:
            filter_param = f'{replication_key} ge {filter_value}'
            self.params = {"$orderby": orderby_param, "$filter": filter_param}
        else:
            self.params = {"$orderby": orderby_param}

    def modify_object(self, record: Dict, parent_record: Dict = None) -> Dict:
        """
        Modify the record before writing to the stream
        """
        return record

    def get_url_endpoint(self, parent_obj: Dict = None) -> str:
        """
        Get the URL endpoint for the stream
        """
        return self.url_endpoint or f"{self.client.base_url}/{self.path}"


class IncrementalStream(BaseStream):
    """Base Class for Incremental Stream."""
    replication_method = "INCREMENTAL"

    def _resolve_replication_key(self, key: Any = None) -> str:
        """Return key if provided, otherwise fall back to replication_keys[0].

        Raises:
            ValueError: If key is not provided and replication_keys is empty.
        """
        if key:
            return key
        if not self.replication_keys:
            raise ValueError(
                f"Stream '{self.tap_stream_id}' is misconfigured: "
                "'replication_keys' must not be empty for an INCREMENTAL stream."
            )
        return self.replication_keys[0]

    def get_bookmark(self, state: dict, stream: str, key: Any = None) -> int:
        """A wrapper for singer.get_bookmark to deal with compatibility for
        bookmark values or start values."""
        return get_bookmark(
            state,
            stream,
            self._resolve_replication_key(key),
            self.client.config["start_date"],
        )

    def write_bookmark(self, state: dict, stream: str, key: Any = None, value: Any = None) -> Dict:
        """A wrapper for singer.write_bookmark to deal with compatibility for
        bookmark values or start values."""
        resolved_key = self._resolve_replication_key(key)
        if not resolved_key:
            return state

        current_bookmark = get_bookmark(state, stream, resolved_key, self.client.config["start_date"])
        value = max(current_bookmark, value)
        return write_bookmark(
            state, stream, resolved_key, value
        )


    def sync(
        self,
        state: Dict,
        transformer: Transformer,
        parent_obj: Dict = None,
    ) -> Dict:
        """Implementation for `type: Incremental` stream."""
        bookmark_date = self.get_bookmark(state, self.tap_stream_id)
        current_max_bookmark_date = bookmark_date
        secondary_orderby_key = None
        # `incident` records frequently share identical `modifiedon` timestamps due to
        # bulk updates (case merges, SLA recalculations, workflow triggers). Adding the
        # primary key as a secondary sort ensures a stable page order and prevents the
        # OData $skiptoken cursor from skipping or duplicating records at page boundaries.
        if self.tap_stream_id == 'incident' and self.key_properties:
            secondary_orderby_key = self.key_properties[0]

        self.update_params(
            orderby_key=self.replication_keys[0],
            replication_key=self.replication_keys[0],
            filter_value=bookmark_date,
            secondary_orderby_key=secondary_orderby_key
        )
        self.update_header(Prefer=f'odata.maxpagesize={self.page_size}')
        self.url_endpoint = self.get_url_endpoint(parent_obj)

        with metrics.record_counter(self.tap_stream_id) as counter:
            for record in self.get_records():
                record = self.modify_object(record, parent_obj)
                transformed_record = transformer.transform(
                    record, self.schema, self.metadata
                )

                record_bookmark = transformed_record[self.replication_keys[0]]
                if record_bookmark >= bookmark_date:
                    if self.is_selected():
                        write_record(self.tap_stream_id, transformed_record)
                        counter.increment()

                    current_max_bookmark_date = max(
                        current_max_bookmark_date, record_bookmark
                    )

                    for child in self.child_to_sync:
                        child.sync(state=state, transformer=transformer, parent_obj=record)

            state = self.write_bookmark(state, self.tap_stream_id, value=current_max_bookmark_date)
            return counter.value


class FullTableStream(BaseStream):
    """Base Class for Incremental Stream."""
    replication_method = "FULL_TABLE"
    replication_keys = []

    def sync(
        self,
        state: Dict,
        transformer: Transformer,
        parent_obj: Dict = None,
    ) -> Dict:
        """Abstract implementation for `type: Fulltable` stream."""
        self.url_endpoint = self.get_url_endpoint(parent_obj)
        self.update_header(Prefer=f'odata.maxpagesize={self.page_size}')

        with metrics.record_counter(self.tap_stream_id) as counter:
            for record in self.get_records():
                transformed_record = transformer.transform(
                    record, self.schema, self.metadata
                )
                if self.is_selected():
                    write_record(self.tap_stream_id, transformed_record)
                    counter.increment()

                for child in self.child_to_sync:
                    child.sync(state=state, transformer=transformer, parent_obj=record)

            return counter.value


class ParentBaseStream(IncrementalStream):
    """Base Class for Parent Stream."""

    def get_bookmark(self, state: Dict, stream: str, key: Any = None) -> int:
        """A wrapper for singer.get_bookmark to deal with compatibility for
        bookmark values or start values."""

        min_parent_bookmark = (
            super().get_bookmark(state, stream) if self.is_selected() else None
        )
        for child in self.child_to_sync:
            bookmark_key = f"{self.tap_stream_id}_{self.replication_keys[0]}"
            child_bookmark = super().get_bookmark(
                state, child.tap_stream_id, key=bookmark_key
            )
            min_parent_bookmark = (
                min(min_parent_bookmark, child_bookmark)
                if min_parent_bookmark
                else child_bookmark
            )

        return min_parent_bookmark

    def write_bookmark(
        self, state: Dict, stream: str, key: Any = None, value: Any = None
    ) -> Dict:
        """A wrapper for singer.get_bookmark to deal with compatibility for
        bookmark values or start values."""
        if self.is_selected():
            super().write_bookmark(state, stream, value=value)

        for child in self.child_to_sync:
            bookmark_key = f"{self.tap_stream_id}_{self.replication_keys[0]}"
            super().write_bookmark(
                state, child.tap_stream_id, key=bookmark_key, value=value
            )

        return state


class ChildBaseStream(IncrementalStream):
    """Base Class for Child Stream."""

    def get_url_endpoint(self, parent_obj=None):
        """Prepare URL endpoint for child streams."""
        return f"{self.client.base_url}/{self.path.format(parent_obj['id'])}"

    def get_bookmark(self, state: Dict, stream: str, key: Any = None) -> int:
        """Singleton bookmark value for child streams."""
        if not self.bookmark_value:
            self.bookmark_value = super().get_bookmark(state, stream)

        return self.bookmark_value
