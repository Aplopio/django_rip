from abc import ABCMeta

import six

from rip.schema.default_field_value import DEFAULT_FIELD_VALUE
from rip.schema.validation_result import ValidationResult
class FieldTypes(object):
    READONLY = 'readonly'
    DEFAULT = 'default'
    IMMUTABLE = 'immutable'


class BaseField(six.with_metaclass(ABCMeta)):

    def __init__(self, required=False,
                 field_type=FieldTypes.DEFAULT,
                 nullable=True,
                 entity_attribute=None,
                 show_in_list=True):
        self.entity_attribute = entity_attribute
        self.nullable = nullable
        self.required = required
        self.field_type = field_type
        self.show_in_list = show_in_list

    def validate(self, request, value):
        """
        This is not for business validation
        This should be only used for type validation
        Hence the only input is the value of the field
        :param value:
        :return:
        """
        if self.required and value == DEFAULT_FIELD_VALUE:
            return ValidationResult(is_success=False,
                                    reason='This field is required')
        if not self.nullable and value is None:
            return ValidationResult(is_success=False,
                                    reason='null is not a valid value')
        return ValidationResult(is_success=True)

    def serialize(self, request, value):
        return value

    def clean(self, request, value):
        """
        Called during update and create
        If there are deeper nesting within a field,
        which may have readonly fields, this function
        will be overridden
        :param request:
        :param value:
        :return:
        """
        return value


class DictionaryField(BaseField):
    field_type = dict
