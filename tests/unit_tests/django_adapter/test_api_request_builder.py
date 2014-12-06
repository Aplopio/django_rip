import unittest
from  django import conf
from hamcrest import assert_that
from hamcrest.core.core.isequal import equal_to
from hamcrest.library.collection.isdict_containing import has_entry
from mock import MagicMock, patch

from rip.django_adapter import metadata_factory
from rip.django_adapter import api_request_builder


class TestBuildApiRequest(unittest.TestCase):
    def setUp(self):
        import os
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    @patch.object(conf, 'settings')
    @patch.object(metadata_factory, 'api_breadcrumb_filters')
    @patch.object(metadata_factory, 'api_breadcrumbs')
    def test_create_request_with_right_request_params(self,
                                                      parent_breadcrumbs_from,
                                                      breadcrumb_filters,
                                                      settings):
        http_request = MagicMock()
        mock_api = MagicMock()
        mock_api.name = 'api_name'
        mock_api.version = '1.0.0.1'
        mock_user = http_request.user
        request_body = MagicMock()
        http_request.user.is_anonymous.return_value = False
        breadcrumb_filters.return_value = expected_req_params = {'bar': 'baz'}

        request = api_request_builder.build_request(http_request=http_request,
                                                    url='candidates',
                                                    api=mock_api,
                                                    request_data={},
                                                    request_body=request_body)
        assert_that(request.user, equal_to(mock_user))
        assert_that(request.request_params, equal_to(expected_req_params))


    @patch.object(conf, 'settings')
    @patch.object(metadata_factory, 'api_breadcrumb_filters')
    @patch.object(metadata_factory, 'api_breadcrumbs')
    def test_create_request_with_right_context_params(self,
                                                      parent_breadcrumbs_from,
                                                      api_breadcrumb_filters,
                                                      settings):
        http_request = MagicMock()
        mock_api = MagicMock()
        mock_api.name = 'api_name'
        mock_api.version = '1.0.0.1'
        http_request.user.is_anonymous.return_value = False
        request_body = MagicMock()
        settings.TIME_ZONE = expected_timezone = MagicMock()

        request = api_request_builder.build_request(http_request=http_request,
                                                    url='candidates',
                                                    api=mock_api,
                                                    request_data={},
                                                    request_body=request_body)

        assert_that(request.context_params, has_entry('protocol', 'http'))
        assert_that(request.context_params, has_entry('url', 'candidates'))
        assert_that(request.context_params,
                    has_entry('timezone', expected_timezone))
        assert_that(request.context_params,
                    has_entry('api_version', mock_api.version))
        assert_that(request.context_params,
                    has_entry('api_name', mock_api.name))

    @patch.object(conf, 'settings')
    @patch.object(metadata_factory, 'api_breadcrumb_filters')
    @patch.object(metadata_factory, 'api_breadcrumbs')
    def test_create_request_with_anonymous_user(self,
                                                parent_breadcrumbs_from,
                                                api_breadcrumb_filters,
                                                settings):
        http_request = MagicMock()
        mock_api = MagicMock()
        http_request.user.is_anonymous.return_value = True
        request_body = MagicMock()
        request = api_request_builder.build_request(http_request=http_request,
                                                    url='candidates',
                                                    api=mock_api,
                                                    request_data={},
                                                    request_body=request_body)
        assert_that(request.user, equal_to(None))


    def test_create_request_with_custom_headers(self):
        http_request = MagicMock()
        mock_api = MagicMock()
        meta = dict(HTTP_CUSTOM_HEADER='custom_value')
        http_request.META = meta
        request_body = MagicMock()
        request = api_request_builder.build_request(http_request=http_request,
                                                    url='candidates',
                                                    api=mock_api,
                                                    request_data={},
                                                    request_body=request_body)
        assert_that(request.request_headers, has_entry('HTTP_CUSTOM_HEADER',
                                                       'custom_value'))


    def test_create_request_with_request_body(self):
        http_request = MagicMock()
        mock_api = MagicMock()
        request_body = 'abcd'
        request = api_request_builder.build_request(http_request=http_request,
                                                    url='candidates',
                                                    api=mock_api,
                                                    request_data={},
                                                    request_body=request_body)
        assert_that(request.request_body, equal_to('abcd'))

