import unittest
from rip.schema.list_field import ListField
from rip.schema.string_field import StringField


class TestValidateListField(unittest.TestCase):
    def test_return_success_if_nullable_and_value_is_none(self):
        field = ListField(field=StringField(), nullable=True)

        result = field.validate(request=None, value=None)

        assert result.is_success

    def test_return_failure_if_nullable_and_value_is_none(self):
        field = ListField(field=StringField(), nullable=False)

        result = field.validate(request=None, value=None)

        assert not result.is_success

    def test_return_failure_if_value_is_not_a_list(self):
        field = ListField(field=StringField(), nullable=False)

        result = field.validate(request=None, value='blah')

        assert not result.is_success

    def test_return_success_if_validation_passes(self):

        field = ListField(field=StringField(), nullable=True)

        result = field.validate(request=None, value=['foo', None])

        assert result.is_success

    def test_return_success_if_validation_fails_on_child_field(self):

        field = ListField(field=StringField(), nullable=False)

        result = field.validate(request=None, value=['foo', None])

        assert not result.is_success
        assert isinstance(result.reason, list)
        assert len(result.reason) == 1
