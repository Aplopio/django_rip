# -*- coding: utf-8 -*-
from rip.schema.default_field_value import DEFAULT_FIELD_VALUE

from rip.schema.base_field import BaseField, FieldTypes
from rip.schema.validation_result import ValidationResult


class ChoiceField(BaseField):
    """Restrict the value which is received.
    """
    def __init__(self, choices, entity_attribute=None, required=False,
                 field_type=FieldTypes.DEFAULT):
        """Pass list of allowed values.

        :param choices: `list` or `tuple` or `set` of values.

        Usage:
        -----
        >>>choice_field = ChoiceField(choices=(1, 2))
        >>>result = choice_field.validate(request=None, value=3)
        >>>result.is_success
        False

        >>>result = choice_field.validate(request=None, value=1)
        >>>result.is_success
        True

        >>>choice_field = ChoiceField(choices=[1, 2], required=True)
        >>>from rip.schema.default_field_value import DEFAULT_FIELD_VALUE
        >>>result = choice_field.validate(request=None, value=DEFAULT_FIELD_VALUE)
        >>>assert result.is_success
        False
        >>>result.reason
        'This field is required'

        >>>result = choice_field.validate(request=None, value=1)
        >>>result.is_success
        True
        """
        super(ChoiceField, self).__init__(
            required=required, field_type=field_type,
            entity_attribute=entity_attribute)

        self.choices = choices

    def _validate_choices_type(self):
        allowed_types = (list, tuple, set, )
        # Prohibit user from giving any data type in choices attribute
        msg = u"choices: {} should of any one of the type {}".format(
            self.choices, allowed_types)

        if not isinstance(self.choices, allowed_types):
            return ValidationResult(is_success=False, reason=msg)
        return ValidationResult(is_success=True)

    def validate(self, request, value):
        validation_result = super(ChoiceField, self).validate(request, value)

        if not validation_result.is_success:
            return validation_result
        if value == DEFAULT_FIELD_VALUE:
            return ValidationResult(is_success=True)

        # Check it is possible to do validation.
        result = self._validate_choices_type()

        if not result.is_success:
            return result

        if value in self.choices:
            return ValidationResult(is_success=True)
        return ValidationResult(
            is_success=False, reason=u"{} isn't valid choice".format(value))
