import unittest

from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to

from rip.schema.url_field import UrlField
from rip.schema.default_field_value import \
    DEFAULT_FIELD_VALUE


class TestUrlField(unittest.TestCase):
    def test_validate_returns_error_if_required_and_value_is_default(self):
        url_field = UrlField(required=True)

        result = url_field.validate(None, DEFAULT_FIELD_VALUE)

        assert_that(result.is_success, equal_to(False))
        assert_that(result.reason, equal_to('This field is required'))

    def test_validate_returns_error_for_invalid_type(self):
        url_field = UrlField(required=True)

        result = url_field.validate(None, 1212)

        assert_that(result.is_success, equal_to(False))
        assert_that(result.reason, equal_to('Expected type string'))

    def test_validate_returns_error_if_url_is_invalid(self):
        url_field = UrlField(required=True)

        result_1 = url_field.validate(None, 'hhhhh')
        result_2 = url_field.validate(None, 'gggg,gggg')

        assert_that(result_1.is_success, equal_to(False))
        assert_that(result_1.reason, equal_to('The url is not valid'))
        assert_that(result_2.is_success, equal_to(False))
        assert_that(result_2.reason, equal_to('The url is not valid'))

    def test_validate_returns_true_for_valid_url(self):
        url_field = UrlField(required=True)

        result_1 = url_field.validate(None, 'something.com')
        result_2 = url_field.validate(None, 'http://ffff.com')
        result_3 = url_field.validate(None, 'https://fsdfsdf.com')

        assert_that(result_1.is_success, equal_to(True))
        assert_that(result_2.is_success, equal_to(True))
        assert_that(result_3.is_success, equal_to(True))

    def test_validate_returns_true_if_field_is_nullable_and_value_none(self):
        url_field = UrlField(nullable=True)

        result = url_field.validate(request=None, value=None)

        assert_that(result.is_success, equal_to(True))
