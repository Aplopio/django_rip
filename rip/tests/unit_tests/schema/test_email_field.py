import unittest
from rip.schema_fields.email_field import EmailField
from rip.schema_fields.default_field_value import \
    DEFAULT_FIELD_VALUE


class TestEmailField(unittest.TestCase):
    def test_validate_returns_error_if_required_and_value_is_default(self):
        email_field = EmailField(required=True)

        result = email_field.validate(None, DEFAULT_FIELD_VALUE)

        assert not result.is_success
        assert result.reason == 'This field is required'

    def test_validate_returns_error_for_invalid_type(self):
        email_field = EmailField(required=True)

        result = email_field.validate(None, 1212)

        assert not result.is_success
        assert result.reason == 'Expected type string'

    def test_validate_returns_error_if_email_is_invalid(self):
        email_field = EmailField(required=True)

        result_1 = email_field.validate(None, 'asd@asd')
        result_2 = email_field.validate(None, 'asd@asd.com,div@kar.co')

        assert not result_1.is_success
        assert result_1.reason == 'Invalid email address'
        assert not result_2.is_success
        assert result_2.reason == 'Invalid email address'

    def test_validate_returns_true_for_valid_email(self):
        email_field = EmailField(required=True)

        result_1 = email_field.validate(None, 'div.me@kar.boo')
        result_2 = email_field.validate(None, 'div@kar.co.in')
        result_3 = email_field.validate(None, 'div@kar.co')

        assert result_1.is_success
        assert result_2.is_success
        assert result_3.is_success

    def test_validate_returns_true_if_field_is_nullable_and_value_none(self):
        email_field = EmailField(nullable=True)

        result = email_field.validate(request=None, value=None)

        assert result.is_success
