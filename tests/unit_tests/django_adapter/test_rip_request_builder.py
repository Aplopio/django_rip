import unittest
from django import conf
from mock import MagicMock, patch
from django.test.client import RequestFactory

from http_adapter.default_rip_request_builder import DefaultRipRequestBuilder
from rip.request import Request
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'


class TestBuildApiRequest(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch.object(conf, 'settings')
    def test_create_request_with_right_request_params(self, settings):
        http_request = self.factory.get('/someurl?getkey=getvalue')
        http_request.user = mock_user = MagicMock()
        http_request.user.is_anonymous.return_value = False
        url_kwargs = {'key': 'value'}
        request_builder = DefaultRipRequestBuilder(
            http_request=http_request, url_kwargs=url_kwargs)

        request = request_builder.build_rip_request_or_response()

        assert isinstance(request, Request)
        assert request.request_params == {'key': 'value', 'getkey': 'getvalue'}

    @patch.object(conf, 'settings')
    def test_create_request_with_right_context_params(self, settings):
        http_request = self.factory.get('/someurl?getkey=getvalue')
        http_request.user = mock_user = MagicMock()
        http_request.user.is_anonymous.return_value = False
        url_kwargs = {'key': 'value'}
        settings.TIME_ZONE = expected_timezone = MagicMock()

        request_builder = DefaultRipRequestBuilder(
            http_request=http_request, url_kwargs=url_kwargs)
        request = request_builder.build_rip_request_or_response()

        assert request.context_params.get('protocol', 'http')
        assert request.context_params.get('timezone', expected_timezone)

    @patch.object(conf, 'settings')
    def test_create_request_with_anonymous_user(self, settings):
        http_request = self.factory.get('/someurl?getkey=getvalue')
        http_request.user = mock_user = MagicMock()
        http_request.user.is_anonymous.return_value = True

        request_builder = DefaultRipRequestBuilder(
            http_request=http_request, url_kwargs={})
        request = request_builder.build_rip_request_or_response()

        assert request.user is None

    def test_create_request_with_custom_headers(self):
        http_request = MagicMock()
        meta = dict(HTTP_CUSTOM_HEADER='custom_value')
        http_request.META = meta

        request_builder = DefaultRipRequestBuilder(
            http_request=http_request, url_kwargs={})
        request = request_builder.build_rip_request_or_response()

        assert request.request_headers.get('HTTP_CUSTOM_HEADER') == \
            'custom_value'

    def test_create_request_with_request_body(self):
        http_request = MagicMock()
        request_body = http_request.read.return_value = 'abcd'

        request_builder = DefaultRipRequestBuilder(
            http_request=http_request, url_kwargs={})
        request = request_builder.build_rip_request_or_response()
        assert request.request_body == request_body
