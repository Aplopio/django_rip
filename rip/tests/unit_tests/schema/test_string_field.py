from unittest.case import TestCase
from rip.schema.string_field import StringField
from rip.schema.default_field_value import \
    DEFAULT_FIELD_VALUE


class TestCharField(TestCase):
    def test_validate_returns_error_if_required_and_value_is_default(self):
        string_field = StringField(10, required=True)

        result = string_field.validate(None, DEFAULT_FIELD_VALUE)

        assert not result.is_success
        assert result.reason == 'This field is required'

    def test_validate_returns_error_for_invalid_type(self):
        string_field = StringField(10, required=True)

        result = string_field.validate(None, 1212)

        assert not result.is_success
        assert result.reason == 'Expected type string'

    def test_validate_returns_error_if_max_length_exceeds(self):
        string_field = StringField(max_length=1, required=True)

        result = string_field.validate(None, '1212')

        assert not result.is_success
        assert result.reason == 'Maxlength of 1 exceeded'

    def test_validate_returns_no_error_when_max_length_is_none(self):
        string_field = StringField(max_length=None, required=True)

        result = string_field.validate(None, '1212' * 1000)

        assert result.is_success

    def test_should_not_raise_if_not_a_required_field(self):
        string_field = StringField(max_length=100, required=False)

        result = string_field.validate(request=None, value=DEFAULT_FIELD_VALUE)

        assert result.is_success

    def test_should_return_true_when_nullable_and_value_is_none(self):
        string_field = StringField(max_length=100, nullable=True)

        result = string_field.validate(request=None, value=None)

        assert result.is_success

    def test_should_return_true_when_blank_is_true_and_value_is_blank(self):
        string_field = StringField()

        result = string_field.validate(request=None, value="")

        assert result.is_success is True

    def test_should_return_false_when_blank_is_false_and_value_is_blank(self):
        string_field = StringField(blank=False)

        result = string_field.validate(request=None, value="")

        assert result.is_success is False
        assert result.reason == "This field is required"

    def test_should_return_true_when_blank_is_false_and_value_is_not_blank(
            self):
        string_field = StringField(blank=False)

        result = string_field.validate(request=None, value="asd")

        assert result.is_success is True

    def test_should_not_strip_value(self):
        string_field = StringField()

        result = string_field.clean(request=None, value=" asd ")

        assert result == ' asd '

    def test_should_strip_value(self):
        string_field = StringField(trim=True)

        result = string_field.clean(request=None, value=' asd ')

        assert result == 'asd'

    def test_should_strip_value_for_given_characters(self):
        string_field = StringField(trim=' ')

        result = string_field.clean(request=None, value=' asd ')

        assert result == 'asd'
