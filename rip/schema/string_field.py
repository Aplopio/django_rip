from rip.schema.base_field import \
    BaseField, FieldTypes
from rip.schema.default_field_value import \
    DEFAULT_FIELD_VALUE
from rip.schema.validation_result import \
    ValidationResult


class StringField(BaseField):
    field_type = unicode

    def __init__(self,
                 max_length=256,
                 required=False,
                 field_type=FieldTypes.DEFAULT,
                 nullable=True,
                 entity_attribute=None,
                 show_in_list=True):
        self.max_length = max_length
        super(StringField, self).__init__(required=required, field_type=field_type,
                                        nullable=nullable,
                                        entity_attribute=entity_attribute,
                                        show_in_list=show_in_list)

    def validate(self, request, value):
        validation_result = super(StringField, self).validate(request, value)

        if not validation_result.is_success:
            return validation_result

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
