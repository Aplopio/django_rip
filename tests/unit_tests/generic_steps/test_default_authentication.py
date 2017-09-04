import unittest

from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from mock import MagicMock

from rip.generic_steps import default_authentication
from rip.request import Request
from rip import error_types


class TestAuthenticationStep(unittest.TestCase):
    def test_authentication_for_a_valid_user(self):
        user = MagicMock()
        request = Request(user=user, request_params=None)

        returned_request = default_authentication.authenticate(request)

        assert_that(returned_request, equal_to(request))

    def test_authentication_when_no_user(self):
        request = Request(user=None, request_params=None)

        response = default_authentication.authenticate(request)

        assert_that(response.is_success, equal_to(False))
        assert_that(response.reason, equal_to(error_types.AuthenticationFailed))


if __name__ == '__main__':
    unittest.main()
