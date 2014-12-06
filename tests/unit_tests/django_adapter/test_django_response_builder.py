import unittest

from mock import MagicMock
import simplejson

from rip.django_adapter import django_response_builder
from rip.response import Response
from rip import error_types


class TestDjangoResponseBuilder(unittest.TestCase):
    def test_should_return_not_authenticated_response_if_auth_fails(self):
        response = Response(is_success=False,
                            reason=error_types.AuthenticationFailed,
                            data={'asdf': 1121})
        http_request = MagicMock()
        http_response = django_response_builder.build_http_response(
            http_request, response)
        self.assertEqual(http_response.status_code, 401)
        self.assertEqual(http_response.content,
                         simplejson.dumps({'asdf': 1121}))

    def test_should_return_bad_request_for_invalid_data(self):
        response = Response(is_success=False,
                            reason=error_types.InvalidData,
                            data={'defg': 1121})
        http_request = MagicMock()
        http_response = django_response_builder.build_http_response(
            http_request, response)
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.content,
                         simplejson.dumps({'defg': 1121}))


if __name__ == '__main__':
    unittest.main()
