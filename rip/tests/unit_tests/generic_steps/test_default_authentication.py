import unittest
from mock import MagicMock

from rip.generic_steps import default_authentication, error_types
from rip.request import Request


class TestAuthenticationStep(unittest.TestCase):
    def test_authentication_for_a_valid_user(self):
        user = MagicMock()
        request = Request(user=user, request_params=None)

        returned_request = default_authentication.authenticate(request)

        assert returned_request == request

    def test_authentication_when_no_user(self):
        request = Request(user=None, request_params=None)

        response = default_authentication.authenticate(request)

        assert not response.is_success
        assert response.reason == error_types.AuthenticationFailed
