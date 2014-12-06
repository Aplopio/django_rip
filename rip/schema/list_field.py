from rip.schema.base_field import BaseField, FieldTypes
from rip.schema.default_field_value import \
    DEFAULT_FIELD_VALUE
from rip.schema.validation_result import \
    ValidationResult


class ListField(BaseField):
    def __init__(self, field, required=False, field_type=FieldTypes.DEFAULT, \
                 nullable=True, show_in_list=True,
                 entity_attribute=None):
        super(ListField, self).__init__(required=required,
                                        field_type=field_type,
                                        nullable=nullable,
                                        entity_attribute=entity_attribute,
                                        show_in_list=show_in_list)
        self.field = field
        self.field.field_type = field_type
        self.field.required = required
        self.field.nullable = nullable

    def validate(self, request, value):
        errors = []

        validation_result = super(ListField, self).validate(request, value)
        if not validation_result.is_success:
            return validation_result

        value = value if value not in (DEFAULT_FIELD_VALUE, None) else []
        for item in value:
            validation_result = self.field.validate(request, item)
            if not validation_result.is_success:
                errors.append(validation_result.reason)

        if errors:
            return ValidationResult(is_success=False, reason=errors)
        else:
            return ValidationResult(is_success=True)

    def clean(self, request, value):
        if value is None:
            return None
        return [self.field.clean(request, item) for item in value]

    def serialize(self, request, value):
        if value is None:
            return None
        return [self.field.serialize(request, item) for item in value]
