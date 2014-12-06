import unittest

from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to

from rip.schema.email_field import EmailField
from rip.schema.default_field_value import \
    DEFAULT_FIELD_VALUE


class TestEmailField(unittest.TestCase):

    def test_validate_returns_error_if_required_and_value_is_default(self):
        email_field = EmailField(required=True)

        result = email_field.validate(None, DEFAULT_FIELD_VALUE)

        assert_that(result.is_success, equal_to(False))
        assert_that(result.reason, equal_to('This field is required'))

    def test_validate_returns_error_for_invalid_type(self):
        email_field = EmailField(required=True)

        result = email_field.validate(None, 1212)

        assert_that(result.is_success, equal_to(False))
        assert_that(result.reason, equal_to('Expected type string'))

    def test_validate_returns_error_if_email_is_invalid(self):
        email_field = EmailField(required=True)

        result_1 = email_field.validate(None, 'asd@asd')
        result_2 = email_field.validate(None, 'asd@asd.com,div@kar.co')

        assert_that(result_1.is_success, equal_to(False))
        assert_that(result_1.reason, equal_to('Invalid email address'))
        assert_that(result_2.is_success, equal_to(False))
        assert_that(result_2.reason, equal_to('Invalid email address'))

    def test_validate_returns_true_for_valid_email(self):
        email_field = EmailField(required=True)

        result_1 = email_field.validate(None, 'div.me@kar.boo')
        result_2 = email_field.validate(None, 'div@kar.co.in')
        result_3 = email_field.validate(None, 'div@kar.co')

        assert_that(result_1.is_success, equal_to(True))
        assert_that(result_2.is_success, equal_to(True))
        assert_that(result_3.is_success, equal_to(True))
