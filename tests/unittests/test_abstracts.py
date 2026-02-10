import unittest
from unittest.mock import MagicMock, patch, call
from tap_ms_dynamics_365_crm.streams.abstracts import BaseStream


class ConcreteStream(BaseStream):
    """Concrete implementation of BaseStream for testing"""
    def sync(self, state, transformer, parent_obj=None):
        """Minimal implementation of abstract sync method"""
        return {}


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
