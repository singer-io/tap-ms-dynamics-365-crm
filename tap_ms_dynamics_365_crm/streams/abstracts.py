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
from tap_ms_dynamics_365_crm.client import Client, MAX_PAGESIZE, AUTH_METHOD_AUTHORIZATION_CODE
from tap_ms_dynamics_365_crm.exceptions import (
    MSDynamics365CrmError,
    MSDynamics365CrmForbiddenError,
    MSDynamics365CrmNotFoundError
)

LOGGER = get_logger()

# Entities that reject a plain collection GET with `Expected non-empty Guid`
# (400) under the `authorization_code` (delegated) auth method -- but ARE
# valid, accessible entity sets there, they just can't be listed without an
# id. For these, under authorization_code, access is confirmed (and records
# are extracted during sync) by fetching the calling user's Dataverse UserId
# (via WhoAmI) and requesting that id directly: a 404 "... Does Not Exist"
# confirms the entity set itself is reachable (the id simply doesn't match a
# record there). Under client_credentials the plain collection GET works
# fine, so this scoping is skipped entirely for that auth method.
SCOPED_ACCESS_CHECK_ENTITIES = {
    'msdyn_requirementdependency',
    'msdyn_incidenttypessetup',
}


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
        if self._uses_scoped_access():
            yield from self._get_scoped_records()
            return

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

    def _uses_scoped_access(self) -> bool:
        """Whether this stream must use the WhoAmI-scoped id lookup instead
        of a plain collection request -- only applies to entities in
        SCOPED_ACCESS_CHECK_ENTITIES under the authorization_code auth
        method (client_credentials can query these entities normally)."""
        return (
            self.tap_stream_id in SCOPED_ACCESS_CHECK_ENTITIES
            and self.client.auth_method == AUTH_METHOD_AUTHORIZATION_CODE
        )

    def _get_current_user_id(self):
        """Fetches the calling user's Dataverse UserId via WhoAmI. Returns
        None (and logs a warning) if it can't be resolved."""
        try:
            who_am_i = self.client.make_request(
                method='GET', endpoint=f"{self.client.base_url}/WhoAmI"
            )
        except MSDynamics365CrmError as exc:
            LOGGER.warning(
                "Could not resolve current user via WhoAmI for stream: %s. "
                "HTTP-Error-Message: '%s'",
                self.tap_stream_id, str(exc),
            )
            return None

        user_id = who_am_i.get('UserId')
        if not user_id:
            LOGGER.warning(
                "WhoAmI response missing UserId for stream: %s.", self.tap_stream_id,
            )
        return user_id

    def _get_scoped_records(self) -> Iterator:
        """Fetches the single record scoped to the calling user's id for
        entities in SCOPED_ACCESS_CHECK_ENTITIES, used in place of the normal
        (unsupported) collection GET. Yields nothing if the id doesn't match
        a record (404 'Does Not Exist')."""
        user_id = self._get_current_user_id()
        if not user_id:
            return

        endpoint = self.get_url_endpoint()
        try:
            record = self.client.make_request(
                method='GET', endpoint=f"{endpoint}({user_id})", headers=self.headers
            )
            yield record
        except MSDynamics365CrmNotFoundError as exc:
            if "does not exist" not in str(exc).lower():
                raise

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

    def check_access(self) -> bool:
        """
        Verifies that the credentials can read at least one record from this
        stream's entity set. Returns False when the entity set isn't plainly
        queryable via a simple GET:
         - 403 Forbidden: credentials lack access to the entity.

        Entities in SCOPED_ACCESS_CHECK_ENTITIES (under authorization_code)
        skip the plain GET entirely and are verified via _check_scoped_access
        instead, which uses a 404 Not Found "... Does Not Exist" response
        as its confirmation signal.
        """
        endpoint = self.get_url_endpoint()

        if self._uses_scoped_access():
            return self._check_scoped_access(endpoint)

        try:
            self.client.make_request(method='GET', endpoint=endpoint, params={'$top': 1})
            return True
        except MSDynamics365CrmForbiddenError as exc:
            LOGGER.warning(
                "Unauthorized Stream: %s, excluding from catalog. HTTP-Error-Message: '%s'",
                self.tap_stream_id, str(exc),
            )
            return False

    def _check_scoped_access(self, endpoint: str) -> bool:
        """
        Confirms access for entities that reject a plain collection GET
        (`Expected non-empty Guid`) but are otherwise valid, queryable entity
        sets. Fetches the calling user's Dataverse UserId via WhoAmI, then
        requests that id directly:
         - 200: entity set and record are both reachable -> access confirmed.
         - 404 "... Does Not Exist": entity set is reachable, the id just
           doesn't match a record there -> access confirmed.
         - Any other error (403, an unrelated 404, etc.): access is not
           confirmed -> exclude the stream.
        """
        user_id = self._get_current_user_id()
        if not user_id:
            return False

        try:
            self.client.make_request(method='GET', endpoint=f"{endpoint}({user_id})")
            return True
        except MSDynamics365CrmNotFoundError as exc:
            if "does not exist" in str(exc).lower():
                return True
            LOGGER.warning(
                "Unqueryable Stream: %s, excluding from catalog. HTTP-Error-Message: '%s'",
                self.tap_stream_id, str(exc),
            )
            return False
        except MSDynamics365CrmForbiddenError as exc:
            LOGGER.warning(
                "Unauthorized Stream: %s, excluding from catalog. HTTP-Error-Message: '%s'",
                self.tap_stream_id, str(exc),
            )
            return False

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
