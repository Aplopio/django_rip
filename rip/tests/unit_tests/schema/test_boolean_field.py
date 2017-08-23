import unittest
from rip.schema.boolean_field import BooleanField
from rip.schema.default_field_value import DEFAULT_FIELD_VALUE


class TestValidateBooleanField(unittest.TestCase):
    def test_return_success_if_nullable_and_value_is_none(self):
        field = BooleanField(nullable=True)

        result = field.validate(request=None, value=None)

        assert result.is_success

    def test_return_success_if_not_nullable_and_value_is_none(self):
        field = BooleanField(nullable=False)

        result = field.validate(request=None, value=None)

        assert not result.is_success
        assert result.reason == 'null is not a valid value'

    def test_return_failure_if_value_is_not_boolean(self):
        field = BooleanField()

        result = field.validate(request=None, value='foo')

        assert not result.is_success
        assert result.reason == 'Expected type Boolean'

    def test_return_success_if_value_is_default(self):
        field = BooleanField()

        result = field.validate(request=None, value=DEFAULT_FIELD_VALUE)

        assert result.is_success