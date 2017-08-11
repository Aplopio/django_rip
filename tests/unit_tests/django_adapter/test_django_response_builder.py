import unittest

import simplejson
from mock import MagicMock

from http_adapter.default_http_response_builder import \
    DefaultHttpResponseBuilder
from rip.generic_steps import error_types
from rip.response import Response


class TestDjangoResponseBuilder(unittest.TestCase):
    def test_should_return_not_authenticated_response_if_auth_fails(self):
        response = Response(is_success=False,
                            reason=error_types.AuthenticationFailed,
                            data={'asdf': 1121})
        http_request = MagicMock()
        django_response_builder = DefaultHttpResponseBuilder(
            http_request, response)
        http_response = django_response_builder.build_http_response()
        self.assertEqual(http_response.status_code, 401)
        self.assertEqual(http_response.content,
                         simplejson.dumps({'asdf': 1121}))

    def test_should_return_bad_request_for_invalid_data(self):
        response = Response(is_success=False,
                            reason=error_types.InvalidData,
                            data={'defg': 1121})
        http_request = MagicMock()
        django_response_builder = DefaultHttpResponseBuilder(
            http_request, response)
        http_response = django_response_builder.build_http_response()

        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.content,
                         simplejson.dumps({'defg': 1121}))
