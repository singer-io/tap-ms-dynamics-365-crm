import unittest
from unittest.mock import MagicMock, patch, call
from tap_ms_dynamics_365_crm.streams.abstracts import BaseStream, IncrementalStream, FullTableStream
from tap_ms_dynamics_365_crm.client import AUTH_METHOD_AUTHORIZATION_CODE, AUTH_METHOD_CLIENT_CREDENTIALS
from tap_ms_dynamics_365_crm.exceptions import (
    MSDynamics365CrmForbiddenError,
    MSDynamics365CrmUnauthorizedError,
    MSDynamics365CrmNotFoundError,
    MSDynamics365CrmMethodNotAllowedError,
)


class ConcreteStream(BaseStream):
    """Concrete implementation of BaseStream for testing"""
    def sync(self, state, transformer, parent_obj=None):
        """Minimal implementation of abstract sync method"""
        return {}


class TestBaseStreamCheckAccess(unittest.TestCase):
    """Test BaseStream.check_access functionality"""

    def _make_stream(self, tap_stream_id="competitor", path="competitors"):
        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {}
        client.base_url = "https://org.api.crm.dynamics.com/api/data/v9.2"
        client.auth_method = AUTH_METHOD_CLIENT_CREDENTIALS
        stream = ConcreteStream(client=client)
        stream.tap_stream_id = tap_stream_id
        stream.path = path
        return stream, client

    def test_check_access_returns_true_on_success(self):
        stream, client = self._make_stream()
        client.make_request.return_value = {"value": []}

        self.assertTrue(stream.check_access())
        client.make_request.assert_called_once_with(
            method='GET',
            endpoint="https://org.api.crm.dynamics.com/api/data/v9.2/competitors",
            params={'$top': 1},
        )

    def test_check_access_returns_false_on_forbidden(self):
        stream, client = self._make_stream(tap_stream_id="some_entity")
        client.make_request.side_effect = MSDynamics365CrmForbiddenError(
            "HTTP-error-code: 403, Error: Forbidden."
        )

        self.assertFalse(stream.check_access())

    def test_check_access_reraises_not_found_errors(self):
        """404s are not treated as a known-unqueryable signature and
        propagate rather than being silently excluded."""
        stream, client = self._make_stream(
            tap_stream_id="attributepicklistvalue", path="attributepicklistvalues"
        )
        client.make_request.side_effect = MSDynamics365CrmNotFoundError(
            "HTTP-error-code: 404, Error Code: 0x80060888, Error: Resource not found "
            "for the segment 'AttributePicklistValues'."
        )

        with self.assertRaises(MSDynamics365CrmNotFoundError):
            stream.check_access()

    def test_check_access_reraises_method_not_allowed_errors(self):
        stream, client = self._make_stream(tap_stream_id="some_entity")
        client.make_request.side_effect = MSDynamics365CrmMethodNotAllowedError(
            "HTTP-error-code: 405, Error: Method Not Allowed."
        )

        with self.assertRaises(MSDynamics365CrmMethodNotAllowedError):
            stream.check_access()

    def test_check_access_reraises_unrelated_errors(self):
        stream, client = self._make_stream(tap_stream_id="some_entity")
        client.make_request.side_effect = MSDynamics365CrmUnauthorizedError(
            "HTTP-error-code: 401, Error: Unauthorized."
        )

        with self.assertRaises(MSDynamics365CrmUnauthorizedError):
            stream.check_access()

    def test_check_access_uses_plain_get_for_scoped_entities_under_client_credentials(self):
        """Entities in SCOPED_ACCESS_CHECK_ENTITIES only need the WhoAmI-based
        scoped check under authorization_code -- under client_credentials the
        plain collection GET works fine, so it's used as normal."""
        stream, client = self._make_stream(
            tap_stream_id="msdyn_incidenttypessetup", path="msdyn_incidenttypessetups"
        )
        client.make_request.return_value = {"value": []}

        self.assertTrue(stream.check_access())
        client.make_request.assert_called_once_with(
            method='GET',
            endpoint="https://org.api.crm.dynamics.com/api/data/v9.2/msdyn_incidenttypessetups",
            params={'$top': 1},
        )


class TestBaseStreamScopedAccessCheck(unittest.TestCase):
    """Test BaseStream._check_scoped_access, used for entities in
    SCOPED_ACCESS_CHECK_ENTITIES (msdyn_requirementdependency,
    msdyn_incidenttypessetup) under the authorization_code auth method, where
    they reject a plain collection GET with a 400 'Expected non-empty Guid'
    but ARE valid, accessible entity sets."""

    def _make_stream(self, tap_stream_id="msdyn_incidenttypessetup", path="msdyn_incidenttypessetups"):
        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {}
        client.base_url = "https://org.api.crm.dynamics.com/api/data/v9.2"
        client.auth_method = AUTH_METHOD_AUTHORIZATION_CODE
        stream = ConcreteStream(client=client)
        stream.tap_stream_id = tap_stream_id
        stream.path = path
        return stream, client

    def test_check_access_scoped_true_on_does_not_exist_404(self):
        """WhoAmI succeeds and the id-scoped request 404s with 'Does Not
        Exist' -- this confirms the entity set is reachable, so access is
        granted even though no record matches the user's id."""
        stream, client = self._make_stream()
        client.make_request.side_effect = [
            {"UserId": "11111111-1111-1111-1111-111111111111", "BusinessUnitId": "bu"},
            MSDynamics365CrmNotFoundError(
                "HTTP-error-code: 404, Error Code: 0x80040217, Error: Entity "
                "'msdyn_incidenttypessetup' With Id = 11111111-1111-1111-1111-111111111111 Does Not Exist"
            ),
        ]

        self.assertTrue(stream.check_access())
        self.assertEqual(client.make_request.call_count, 2)
        who_am_i_call, scoped_call = client.make_request.call_args_list
        self.assertEqual(
            who_am_i_call.kwargs["endpoint"],
            "https://org.api.crm.dynamics.com/api/data/v9.2/WhoAmI",
        )
        self.assertEqual(
            scoped_call.kwargs["endpoint"],
            "https://org.api.crm.dynamics.com/api/data/v9.2/msdyn_incidenttypessetups"
            "(11111111-1111-1111-1111-111111111111)",
        )

    def test_check_access_scoped_true_on_success(self):
        """WhoAmI succeeds and the id-scoped request returns a record (200)
        -- access is confirmed directly."""
        stream, client = self._make_stream(
            tap_stream_id="msdyn_requirementdependency", path="msdyn_requirementdependencies"
        )
        client.make_request.side_effect = [
            {"UserId": "22222222-2222-2222-2222-222222222222"},
            {"msdyn_requirementdependencyid": "22222222-2222-2222-2222-222222222222"},
        ]

        self.assertTrue(stream.check_access())

    def test_check_access_scoped_false_on_who_am_i_failure(self):
        stream, client = self._make_stream()
        client.make_request.side_effect = MSDynamics365CrmForbiddenError(
            "HTTP-error-code: 403, Error: Forbidden."
        )

        self.assertFalse(stream.check_access())
        client.make_request.assert_called_once()

    def test_check_access_scoped_false_on_missing_user_id(self):
        stream, client = self._make_stream()
        client.make_request.return_value = {}

        self.assertFalse(stream.check_access())
        client.make_request.assert_called_once()

    def test_check_access_scoped_false_on_forbidden_scoped_request(self):
        stream, client = self._make_stream()
        client.make_request.side_effect = [
            {"UserId": "33333333-3333-3333-3333-333333333333"},
            MSDynamics365CrmForbiddenError("HTTP-error-code: 403, Error: Forbidden."),
        ]

        self.assertFalse(stream.check_access())

    def test_check_access_scoped_reraises_unrelated_404(self):
        """A 404 that doesn't mention 'Does Not Exist' isn't a confirmed
        signature, so it's treated as inaccessible (excluded) rather than
        silently granted."""
        stream, client = self._make_stream()
        client.make_request.side_effect = [
            {"UserId": "44444444-4444-4444-4444-444444444444"},
            MSDynamics365CrmNotFoundError(
                "HTTP-error-code: 404, Error Code: 0x80060888, Error: Resource not found "
                "for the segment 'msdyn_incidenttypessetups'."
            ),
        ]

        self.assertFalse(stream.check_access())


class TestBaseStreamScopedRecordExtraction(unittest.TestCase):
    """Test BaseStream.get_records/_get_scoped_records for entities in
    SCOPED_ACCESS_CHECK_ENTITIES under authorization_code -- sync must use
    the same WhoAmI + id-scoped GET as check_access, since the normal
    collection GET isn't supported for these entities under that auth
    method."""

    def _make_stream(self, tap_stream_id="msdyn_incidenttypessetup", path="msdyn_incidenttypessetups",
                      auth_method=AUTH_METHOD_AUTHORIZATION_CODE):
        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {}
        client.base_url = "https://org.api.crm.dynamics.com/api/data/v9.2"
        client.auth_method = auth_method
        stream = ConcreteStream(client=client)
        stream.tap_stream_id = tap_stream_id
        stream.path = path
        stream.url_endpoint = stream.get_url_endpoint()
        return stream, client

    def test_get_records_yields_scoped_record_on_success(self):
        stream, client = self._make_stream()
        client.make_request.side_effect = [
            {"UserId": "55555555-5555-5555-5555-555555555555"},
            {"msdyn_incidenttypessetupid": "55555555-5555-5555-5555-555555555555"},
        ]

        records = list(stream.get_records())
        self.assertEqual(records, [{"msdyn_incidenttypessetupid": "55555555-5555-5555-5555-555555555555"}])
        who_am_i_call, scoped_call = client.make_request.call_args_list
        self.assertEqual(
            scoped_call.kwargs["endpoint"],
            "https://org.api.crm.dynamics.com/api/data/v9.2/msdyn_incidenttypessetups"
            "(55555555-5555-5555-5555-555555555555)",
        )

    def test_get_records_yields_nothing_on_does_not_exist_404(self):
        stream, client = self._make_stream()
        client.make_request.side_effect = [
            {"UserId": "66666666-6666-6666-6666-666666666666"},
            MSDynamics365CrmNotFoundError(
                "HTTP-error-code: 404, Error Code: 0x80040217, Error: Entity "
                "'msdyn_incidenttypessetup' With Id = 66666666-6666-6666-6666-666666666666 Does Not Exist"
            ),
        ]

        self.assertEqual(list(stream.get_records()), [])

    def test_get_records_yields_nothing_when_who_am_i_fails(self):
        stream, client = self._make_stream()
        client.make_request.side_effect = MSDynamics365CrmForbiddenError(
            "HTTP-error-code: 403, Error: Forbidden."
        )

        self.assertEqual(list(stream.get_records()), [])
        client.make_request.assert_called_once()

    def test_get_records_reraises_unrelated_404(self):
        stream, client = self._make_stream()
        client.make_request.side_effect = [
            {"UserId": "77777777-7777-7777-7777-777777777777"},
            MSDynamics365CrmNotFoundError(
                "HTTP-error-code: 404, Error Code: 0x80060888, Error: Resource not found "
                "for the segment 'msdyn_incidenttypessetups'."
            ),
        ]

        with self.assertRaises(MSDynamics365CrmNotFoundError):
            list(stream.get_records())

    def test_get_records_uses_normal_pagination_under_client_credentials(self):
        """Under client_credentials, scoped entities fall back to the normal
        paginated collection GET, since it works fine for that auth method."""
        stream, client = self._make_stream(auth_method=AUTH_METHOD_CLIENT_CREDENTIALS)
        client.make_request.return_value = {"value": [{"id": "1"}]}

        records = list(stream.get_records())
        self.assertEqual(records, [{"id": "1"}])
        client.make_request.assert_called_once_with(
            'GET',
            "https://org.api.crm.dynamics.com/api/data/v9.2/msdyn_incidenttypessetups",
            headers=stream.headers,
            params=stream.params,
        )


class TestBaseStreamPagination(unittest.TestCase):
    """Test pagination behavior in BaseStream.get_records"""


    def test_get_records_with_pagination_clears_params(self):
        """Test that pagination follows @odata.nextLink and clears params"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000

        first_page_response = {
            'value': [
                {'id': '1', 'name': 'Record 1'},
                {'id': '2', 'name': 'Record 2'}
            ],
            '@odata.nextLink': 'https://api.example.com/data?$skiptoken=abc123'
        }
        second_page_response = {
            'value': [
                {'id': '3', 'name': 'Record 3'},
                {'id': '4', 'name': 'Record 4'}
            ]
        }

        mock_client.make_request.side_effect = [first_page_response, second_page_response]
        stream = ConcreteStream(client=mock_client)
        stream.url_endpoint = 'https://api.example.com/data'
        stream.params = {'$filter': 'status eq active', '$orderby': 'name asc'}
        stream.data_key = 'value'

        records = list(stream.get_records())
        self.assertEqual(len(records), 4)
        self.assertEqual(records[0]['id'], '1')
        self.assertEqual(records[1]['id'], '2')
        self.assertEqual(records[2]['id'], '3')
        self.assertEqual(records[3]['id'], '4')
        self.assertEqual(mock_client.make_request.call_count, 2)

        first_call = mock_client.make_request.call_args_list[0]
        self.assertEqual(first_call[0][0], 'GET')
        self.assertEqual(first_call[0][1], 'https://api.example.com/data')
        self.assertEqual(first_call[1]['params'], {'$filter': 'status eq active', '$orderby': 'name asc'})

        second_call = mock_client.make_request.call_args_list[1]
        self.assertEqual(second_call[0][0], 'GET')
        self.assertEqual(second_call[0][1], 'https://api.example.com/data?$skiptoken=abc123')
        self.assertEqual(second_call[1]['params'], {})

    def test_get_records_single_page_no_nextlink(self):
        """Test get_records with single page (no @odata.nextLink)"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000

        response = {
            'value': [
                {'id': '1', 'name': 'Record 1'},
                {'id': '2', 'name': 'Record 2'}
            ]
        }

        mock_client.make_request.return_value = response

        stream = ConcreteStream(client=mock_client)
        stream.url_endpoint = 'https://api.example.com/data'
        stream.params = {'$top': '100'}
        stream.data_key = 'value'

        records = list(stream.get_records())

        self.assertEqual(len(records), 2)
        self.assertEqual(mock_client.make_request.call_count, 1)

    def test_get_records_empty_response(self):
        """Test get_records with empty response"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000

        response = {'value': []}
        mock_client.make_request.return_value = response

        stream = ConcreteStream(client=mock_client)
        stream.url_endpoint = 'https://api.example.com/data'
        stream.data_key = 'value'

        records = list(stream.get_records())

        self.assertEqual(len(records), 0)
        self.assertEqual(mock_client.make_request.call_count, 1)

    def test_get_records_multiple_pages(self):
        """Test get_records with multiple pages of pagination"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000

        page1 = {
            'value': [{'id': '1'}],
            '@odata.nextLink': 'https://api.example.com/page2'
        }
        page2 = {
            'value': [{'id': '2'}],
            '@odata.nextLink': 'https://api.example.com/page3'
        }
        page3 = {
            'value': [{'id': '3'}],
            '@odata.nextLink': 'https://api.example.com/page4'
        }
        page4 = {
            'value': [{'id': '4'}]
        }

        mock_client.make_request.side_effect = [page1, page2, page3, page4]

        stream = ConcreteStream(client=mock_client)
        stream.url_endpoint = 'https://api.example.com/data'
        stream.params = {'$orderby': 'id'}
        stream.data_key = 'value'

        records = list(stream.get_records())
        self.assertEqual(len(records), 4)
        self.assertEqual(mock_client.make_request.call_count, 4)
        calls = mock_client.make_request.call_args_list
        self.assertEqual(calls[0][1]['params'], {'$orderby': 'id'})
        self.assertEqual(calls[1][1]['params'], {})
        self.assertEqual(calls[2][1]['params'], {})
        self.assertEqual(calls[3][1]['params'], {})

    def test_get_records_uses_custom_data_key(self):
        """Test get_records respects custom data_key"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000
        response = {
            'results': [
                {'id': '1'},
                {'id': '2'}
            ]
        }
        mock_client.make_request.return_value = response
        stream = ConcreteStream(client=mock_client)
        stream.url_endpoint = 'https://api.example.com/data'
        stream.data_key = 'results'
        records = list(stream.get_records())
        self.assertEqual(len(records), 2)

    def test_get_records_missing_data_key(self):
        """Test get_records when data_key is missing from response"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000
        response = {'other_field': 'some_value'}
        mock_client.make_request.return_value = response
        stream = ConcreteStream(client=mock_client)
        stream.url_endpoint = 'https://api.example.com/data'
        stream.data_key = 'value'
        records = list(stream.get_records())
        self.assertEqual(len(records), 0)

    def test_get_records_preserves_headers(self):
        """Test that get_records passes headers to make_request"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000
        response = {'value': [{'id': '1'}]}
        mock_client.make_request.return_value = response
        stream = ConcreteStream(client=mock_client)
        stream.url_endpoint = 'https://api.example.com/data'
        stream.headers = {
            'Accept': 'application/json',
            'Prefer': 'odata.maxpagesize=100'
        }
        stream.data_key = 'value'
        records = list(stream.get_records())
        call_kwargs = mock_client.make_request.call_args[1]
        self.assertEqual(call_kwargs['headers'], {
            'Accept': 'application/json',
            'Prefer': 'odata.maxpagesize=100'
        })


class TestBaseStreamHelperMethods(unittest.TestCase):
    """Test helper methods in BaseStream"""

    def test_update_header(self):
        """Test update_header method"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000
        stream = ConcreteStream(client=mock_client)
        original_headers = stream.headers.copy()
        stream.update_header(Prefer='odata.maxpagesize=200', CustomHeader='value')

        for key, value in original_headers.items():
            if key not in ['Prefer', 'CustomHeader']:
                self.assertEqual(stream.headers[key], value)

        self.assertEqual(stream.headers['Prefer'], 'odata.maxpagesize=200')
        self.assertEqual(stream.headers['CustomHeader'], 'value')

    def test_update_params_with_filter(self):
        """Test update_params with filter value"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000

        stream = ConcreteStream(client=mock_client)
        stream.update_params(
            orderby_key='createdon',
            replication_key='createdon',
            filter_value='2024-01-01T00:00:00Z'
        )

        self.assertEqual(stream.params['$orderby'], 'createdon asc')
        self.assertEqual(stream.params['$filter'], 'createdon ge 2024-01-01T00:00:00Z')

    def test_update_params_without_filter(self):
        """Test update_params without filter value"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000

        stream = ConcreteStream(client=mock_client)
        stream.update_params(orderby_key='modifiedon')

        self.assertEqual(stream.params['$orderby'], 'modifiedon asc')
        self.assertNotIn('$filter', stream.params)

    def test_is_selected_with_catalog(self):
        """Test is_selected when catalog is set"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000

        stream = ConcreteStream(client=mock_client)
        stream.catalog = MagicMock()
        stream.metadata = {(): {'selected': True}}

        with patch('tap_ms_dynamics_365_crm.streams.abstracts.metadata') as mock_metadata:
            mock_metadata.get.return_value = True
            result = stream.is_selected()
            self.assertTrue(result)

    def test_is_selected_without_catalog(self):
        """Test is_selected when catalog is not set"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000

        stream = ConcreteStream(client=mock_client)
        stream.catalog = None

        result = stream.is_selected()
        self.assertTrue(result)

    def test_write_schema_success(self):
        """Test write_schema delegates to singer.write_schema"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000

        stream = ConcreteStream(client=mock_client)
        stream.tap_stream_id = "account"
        stream.schema = {"type": "object"}
        stream.key_properties = ["accountid"]

        with patch("tap_ms_dynamics_365_crm.streams.abstracts.write_schema") as mock_write_schema:
            stream.write_schema()

        mock_write_schema.assert_called_once_with("account", {"type": "object"}, ["accountid"])

    def test_write_schema_reraises_os_error(self):
        """Test write_schema logs and re-raises OSError from singer.write_schema"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000

        stream = ConcreteStream(client=mock_client)
        stream.tap_stream_id = "account"

        with patch(
            "tap_ms_dynamics_365_crm.streams.abstracts.write_schema",
            side_effect=OSError("disk full"),
        ):
            with self.assertRaises(OSError):
                stream.write_schema()

    def test_update_params_with_distinct_secondary_orderby_key(self):
        """Test update_params appends a secondary orderby key when it differs from the primary"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000

        stream = ConcreteStream(client=mock_client)
        stream.update_params(orderby_key='modifiedon', secondary_orderby_key='incidentid')

        self.assertEqual(stream.params['$orderby'], 'modifiedon asc, incidentid asc')

    def test_modify_object_returns_record_unchanged(self):
        """Test the default modify_object implementation is a no-op passthrough"""
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000

        stream = ConcreteStream(client=mock_client)
        record = {"id": "1"}

        self.assertIs(stream.modify_object(record), record)


class TestResolveReplicationKey(unittest.TestCase):
    """Test IncrementalStream._resolve_replication_key"""

    def test_raises_when_no_key_and_no_replication_keys(self):
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000
        stream = IncrementalStream(client=mock_client)
        stream.tap_stream_id = "account"
        stream.replication_keys = []

        with self.assertRaises(ValueError) as e:
            stream._resolve_replication_key()

        self.assertIn("misconfigured", str(e.exception))

    def test_falls_back_to_first_replication_key(self):
        mock_client = MagicMock()
        mock_client.max_pagesize = 5000
        stream = IncrementalStream(client=mock_client)
        stream.replication_keys = ["modifiedon"]

        self.assertEqual(stream._resolve_replication_key(), "modifiedon")


class TestIncrementalStreamBookmarksAndSync(unittest.TestCase):
    """Test IncrementalStream.write_bookmark and IncrementalStream.sync"""

    def _make_stream(self, tap_stream_id="incident"):
        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {"start_date": "2024-01-01T00:00:00Z"}
        client.base_url = "https://org.api.crm.dynamics.com/api/data/v9.2"
        stream = IncrementalStream(client=client)
        stream.tap_stream_id = tap_stream_id
        stream.path = f"{tap_stream_id}s"
        return stream

    def test_write_bookmark_returns_state_unchanged_when_key_not_resolvable(self):
        """When the resolved replication key is falsy, write_bookmark is a no-op"""
        stream = self._make_stream()
        stream.replication_keys = [""]
        state = {"existing": "value"}

        result = stream.write_bookmark(state, stream.tap_stream_id, value="2024-01-01T00:00:00Z")

        self.assertEqual(result, state)

    @patch("tap_ms_dynamics_365_crm.streams.abstracts.write_record")
    @patch("tap_ms_dynamics_365_crm.streams.abstracts.write_bookmark")
    @patch("tap_ms_dynamics_365_crm.streams.abstracts.get_bookmark")
    def test_sync_writes_selected_records_and_syncs_children(
        self, mock_get_bookmark, mock_write_bookmark, mock_write_record
    ):
        mock_get_bookmark.return_value = "2024-01-01T00:00:00Z"
        mock_write_bookmark.return_value = {"bookmarks": {}}

        stream = self._make_stream(tap_stream_id="incident")
        stream.replication_keys = ["modifiedon"]
        stream.key_properties = ["incidentid"]
        stream.catalog = MagicMock()

        record = {"incidentid": "1", "modifiedon": "2024-06-01T00:00:00Z"}
        mock_child = MagicMock()
        stream.child_to_sync = [mock_child]

        mock_transformer = MagicMock()
        mock_transformer.transform.return_value = record

        with patch.object(stream, "get_records", return_value=iter([record])), \
                patch("tap_ms_dynamics_365_crm.streams.abstracts.metadata.get", return_value=True):
            result = stream.sync(state={}, transformer=mock_transformer)

        mock_write_record.assert_called_once_with("incident", record)
        mock_child.sync.assert_called_once_with(state={}, transformer=mock_transformer, parent_obj=record)
        mock_write_bookmark.assert_called_once()
        self.assertEqual(result, 1)


class TestFullTableStreamSync(unittest.TestCase):
    """Test FullTableStream.sync"""

    @patch("tap_ms_dynamics_365_crm.streams.abstracts.write_record")
    def test_sync_writes_selected_records_and_syncs_children(self, mock_write_record):
        client = MagicMock()
        client.max_pagesize = 5000
        client.base_url = "https://org.api.crm.dynamics.com/api/data/v9.2"

        stream = FullTableStream(client=client)
        stream.tap_stream_id = "competitor"
        stream.path = "competitors"
        stream.catalog = MagicMock()

        record = {"competitorid": "1"}
        mock_child = MagicMock()
        stream.child_to_sync = [mock_child]

        mock_transformer = MagicMock()
        mock_transformer.transform.return_value = record

        with patch.object(stream, "get_records", return_value=iter([record])), \
                patch("tap_ms_dynamics_365_crm.streams.abstracts.metadata.get", return_value=True):
            result = stream.sync(state={}, transformer=mock_transformer)

        mock_write_record.assert_called_once_with("competitor", record)
        mock_child.sync.assert_called_once_with(state={}, transformer=mock_transformer, parent_obj=record)
        self.assertEqual(result, 1)


class TestParentBaseStream(unittest.TestCase):
    """Test ParentBaseStream.get_bookmark and ParentBaseStream.write_bookmark"""

    def _make_parent(self):
        from tap_ms_dynamics_365_crm.streams.abstracts import ParentBaseStream

        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {"start_date": "2024-01-01T00:00:00Z"}
        parent = ParentBaseStream(client=client)
        parent.tap_stream_id = "account"
        parent.replication_keys = ["modifiedon"]
        parent.catalog = MagicMock()
        return parent

    @patch("tap_ms_dynamics_365_crm.streams.abstracts.get_bookmark")
    def test_get_bookmark_merges_own_and_child_bookmarks(self, mock_get_bookmark):
        parent = self._make_parent()
        child = MagicMock()
        child.tap_stream_id = "contact"
        parent.child_to_sync = [child]

        mock_get_bookmark.side_effect = ["2024-06-01T00:00:00Z", "2024-01-01T00:00:00Z"]

        with patch("tap_ms_dynamics_365_crm.streams.abstracts.metadata.get", return_value=True):
            result = parent.get_bookmark({}, "account")

        self.assertEqual(result, "2024-01-01T00:00:00Z")

    @patch("tap_ms_dynamics_365_crm.streams.abstracts.write_bookmark")
    def test_write_bookmark_writes_own_and_child_bookmarks(self, mock_write_bookmark):
        parent = self._make_parent()
        child = MagicMock()
        child.tap_stream_id = "contact"
        parent.child_to_sync = [child]

        with patch("tap_ms_dynamics_365_crm.streams.abstracts.metadata.get", return_value=True):
            result = parent.write_bookmark({}, "account", value="2024-06-01T00:00:00Z")

        self.assertEqual(mock_write_bookmark.call_count, 2)
        self.assertEqual(result, {})


class TestChildBaseStream(unittest.TestCase):
    """Test ChildBaseStream.get_url_endpoint and ChildBaseStream.get_bookmark"""

    def _make_child(self):
        from tap_ms_dynamics_365_crm.streams.abstracts import ChildBaseStream

        client = MagicMock()
        client.max_pagesize = 5000
        client.config = {"start_date": "2024-01-01T00:00:00Z"}
        client.base_url = "https://org.api.crm.dynamics.com/api/data/v9.2"
        child = ChildBaseStream(client=client)
        child.tap_stream_id = "contact"
        child.path = "accounts({})/contacts"
        child.replication_keys = ["modifiedon"]
        return child

    def test_get_url_endpoint_formats_parent_id_into_path(self):
        child = self._make_child()

        endpoint = child.get_url_endpoint(parent_obj={"id": "abc-123"})

        self.assertEqual(
            endpoint, "https://org.api.crm.dynamics.com/api/data/v9.2/accounts(abc-123)/contacts"
        )

    @patch("tap_ms_dynamics_365_crm.streams.abstracts.get_bookmark")
    def test_get_bookmark_caches_value_across_calls(self, mock_get_bookmark):
        child = self._make_child()
        mock_get_bookmark.return_value = "2024-01-01T00:00:00Z"

        first = child.get_bookmark({}, "contact")
        second = child.get_bookmark({}, "contact")

        self.assertEqual(first, "2024-01-01T00:00:00Z")
        self.assertEqual(second, "2024-01-01T00:00:00Z")
        mock_get_bookmark.assert_called_once()
