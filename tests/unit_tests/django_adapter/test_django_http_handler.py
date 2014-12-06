import json

from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
from django.utils import unittest
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from mock import MagicMock, patch

from rip.django_adapter import django_response_builder, \
    action_resolver, django_http_handler
from rip.django_adapter import api_request_builder


class DjangoHttpHandler(unittest.TestCase):
    @patch.object(api_request_builder, 'build_request')
    @patch.object(django_response_builder, 'build_http_response')
    @patch.object(action_resolver, 'resolve_action')
    @patch.object(action_resolver, 'is_valid_resource')
    def test_handle_api_call_for_unhandled_action(self,
                                                  mock_is_valid_resource,
                                                  mock_resolve_action,
                                                  mock_build_response,
                                                  mock_build_request):
        mock_is_valid_resource.return_value = True
        mock_resolve_action.return_value = None

        mock_http_request = MagicMock()
        mock_api = MagicMock()

        response = django_http_handler.handle_api_call(
            mock_http_request, 'test_endpoint', mock_api)

        mock_is_valid_resource.assert_called_once_with('test_endpoint',
                                                       mock_api)
        mock_resolve_action.assert_called_once_with(mock_http_request,
                                                    'test_endpoint', mock_api)
        self.assertIsInstance(response, HttpResponseNotAllowed)

    @patch.object(api_request_builder, 'build_request_data')
    @patch.object(action_resolver, 'resolve_action')
    @patch.object(action_resolver, 'is_valid_resource')
    def test_handle_api_call_for_bad_json_data(self,
                                               mock_is_valid_resource,
                                               mock_resolve_action,
                                               mock_build_request_data):
        mock_is_valid_resource.return_value = True
        mock_resolve_action.return_value = MagicMock()
        mock_build_request_data.return_value = expected_request_data = {
            'error_message': 'Expected } at line 3'}

        mock_http_request = MagicMock()
        mock_api = MagicMock()
        mock_http_request.META = http_request_meta = MagicMock()
        mock_http_request.read.return_value = request_body = MagicMock()


        response = django_http_handler.handle_api_call(
            mock_http_request, 'test_endpoint', mock_api)

        mock_is_valid_resource.assert_called_once_with('test_endpoint',
                                                       mock_api)
        mock_resolve_action.assert_called_once_with(mock_http_request,
                                                    'test_endpoint', mock_api)
        mock_build_request_data.assert_called_once_with(request_body, http_request_meta)
        self.assertIsInstance(response, HttpResponseBadRequest)
        assert json.loads(response.content) == expected_request_data

    @patch.object(api_request_builder, 'build_request_data')
    @patch.object(api_request_builder, 'build_request')
    @patch.object(django_response_builder, 'build_http_response')
    @patch.object(action_resolver, 'resolve_action')
    @patch.object(action_resolver, 'is_valid_resource')
    def test_handle_api_call(self,
                             mock_is_valid_resource,
                             mock_resolve_action,
                             mock_build_response,
                             mock_build_request,
                             mock_build_request_data):
        mock_is_valid_resource.return_value = True
        mock_resolve_action.return_value = expected_action = MagicMock()
        expected_action.return_value = expected_response = MagicMock()
        mock_build_request.return_value = expected_request = MagicMock()
        mock_build_response.return_value = expected_http_response = MagicMock()
        mock_build_request_data.return_value = expected_request_data = {}
        mock_http_request = MagicMock()
        mock_http_request.read.return_value = request_body = MagicMock()
        mock_api = MagicMock()
        url = 'test_endpoint'

        http_response = django_http_handler.handle_api_call(
            mock_http_request, url, mock_api)

        mock_is_valid_resource.assert_called_once_with('test_endpoint',
                                                       mock_api)
        mock_resolve_action.assert_called_once_with(mock_http_request,
                                                    'test_endpoint',
                                                    mock_api)
        mock_build_request.assert_called_once_with(
            http_request=mock_http_request,
            url=url, api=mock_api, request_data=expected_request_data,
            request_body=request_body)
        expected_action.assert_called_once_with(expected_request)
        assert_that(http_response, equal_to(expected_http_response))
        mock_build_response.assert_called_once_with(mock_http_request,
                                                    expected_response)

