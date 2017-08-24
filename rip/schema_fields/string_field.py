from rip.schema_fields.base_field import \
    BaseField
from rip.schema_fields.field_types import FieldTypes
from rip.schema_fields.default_field_value import \
    DEFAULT_FIELD_VALUE
from rip.schema_fields.validation_result import \
    ValidationResult


class StringField(BaseField):
    field_type = unicode

    def __init__(
            self, max_length=256, required=False,
            field_type=FieldTypes.DEFAULT, nullable=True,
            entity_attribute=None, show_in_list=True,
            blank=True, trim=False):

        self.max_length = max_length
        self.blank = blank
        self.trim = trim
        super(StringField, self).__init__(
            required=required, field_type=field_type, nullable=nullable,
            entity_attribute=entity_attribute, show_in_list=show_in_list)

    def validate(self, request, value):
        validation_result = super(StringField, self).validate(request, value)

        if not validation_result.is_success:
            return validation_result

        if self.blank is False and not value:
            return ValidationResult(
                is_success=False, reason='This field is required')

        if value == DEFAULT_FIELD_VALUE:
            return ValidationResult(is_success=True)
        if value is None and self.nullable:
            return ValidationResult(is_success=True)

        if not isinstance(value, basestring):
            return ValidationResult(is_success=False,
                                    reason=u'Expected type string')
        if self.max_length and len(value) > self.max_length:
            return ValidationResult(is_success=False,
                                    reason=u'Maxlength of {} exceeded' \
                                    .format(self.max_length))
        return ValidationResult(is_success=True)

    def clean(self, request, value):
        value = super(StringField, self).clean(request, value)
        if self.trim is True:
            return value.strip()
        elif self.trim:
            return value.strip(self.trim)
        else:
            return value



