import unittest
from rip.schema_fields.url_field import UrlField
from rip.schema_fields.default_field_value import \
    DEFAULT_FIELD_VALUE


class TestUrlField(unittest.TestCase):
    def test_validate_returns_error_if_required_and_value_is_default(self):
        url_field = UrlField(required=True)

        result = url_field.validate(None, DEFAULT_FIELD_VALUE)

        assert not result.is_success
        assert result.reason == 'This field is required'

    def test_validate_returns_error_for_invalid_type(self):
        url_field = UrlField(required=True)

        result = url_field.validate(None, 1212)

        assert not result.is_success
        assert result.reason == 'Expected type string'

    def test_validate_returns_error_if_url_is_invalid(self):
        url_field = UrlField(required=True)

        result_1 = url_field.validate(None, 'hhhhh')
        result_2 = url_field.validate(None, 'gggg,gggg')

        assert not result_1.is_success
        assert result_1.reason == 'The url is not valid'
        assert not result_2.is_success
        assert result_2.reason == 'The url is not valid'

    def test_validate_returns_true_for_valid_url(self):
        url_field = UrlField(required=True)

        result_1 = url_field.validate(None, 'something.com')
        result_2 = url_field.validate(None, 'http://ffff.com')
        result_3 = url_field.validate(None, 'https://fsdfsdf.com')

        assert result_1.is_success
        assert result_2.is_success
        assert result_3.is_success

    def test_validate_returns_true_if_field_is_nullable_and_value_none(self):
        url_field = UrlField(nullable=True)

        result = url_field.validate(request=None, value=None)

        assert result.is_success

