from unittest.case import TestCase

from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to

from rip.schema.string_field import StringField
from rip.schema.default_field_value import \
    DEFAULT_FIELD_VALUE


class TestCharField(TestCase):
    def test_validate_returns_error_if_required_and_value_is_default(self):
        charfield = StringField(10, required=True)

        result = charfield.validate(None, DEFAULT_FIELD_VALUE)

        assert_that(result.is_success, equal_to(False))
        assert_that(result.reason, equal_to('This field is required'))

    def test_validate_returns_error_for_invalid_type(self):
        charfield = StringField(10, required=True)

        result = charfield.validate(None, 1212)

        assert_that(result.is_success, equal_to(False))
        assert_that(result.reason, equal_to('Expected type string'))

    def test_validate_returns_error_if_max_length_exceeds(self):
        charfield = StringField(max_length=1, required=True)

        result = charfield.validate(None, '1212')

        assert_that(result.is_success, equal_to(False))
        assert_that(result.reason, equal_to('Maxlength of 1 exceeded'))

    def test_validate_returns_no_error_when_max_length_is_none(self):
        charfield = StringField(max_length=None, required=True)

        result = charfield.validate(None, '1212'* 1000)

        assert_that(result.is_success, equal_to(True))

    def test_should_not_raise_if_not_a_required_field(self):
        charfield = StringField(max_length=100, required=False)

        result = charfield.validate(request=None, value=DEFAULT_FIELD_VALUE)

        assert_that(result.is_success, equal_to(True))
