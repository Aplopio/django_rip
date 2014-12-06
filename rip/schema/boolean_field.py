from rip.schema.base_field import \
    BaseField
from rip.schema.default_field_value import \
    DEFAULT_FIELD_VALUE
from rip.schema.validation_result import \
    ValidationResult


class BooleanField(BaseField):
    field_type = bool

    def validate(self, request, value):
        validation_result = super(BooleanField, self).validate(request, value)
        if not validation_result.is_success:
            return validation_result
        if value == DEFAULT_FIELD_VALUE:
            return ValidationResult(is_success=True)
        if not isinstance(value, bool):
            return ValidationResult(is_success=False,
                                    reason='Expected type Boolean')
        return ValidationResult(is_success=True)