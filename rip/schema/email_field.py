import re

from rip.schema.string_field import StringField
from rip.schema.default_field_value import DEFAULT_FIELD_VALUE
from rip.schema.validation_result import ValidationResult


class EmailValidator(object):
    regex = None

    def __new__(cls, *args):
        if cls.regex is None:
            cls.regex = re.compile(
                r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
                # quoted-string, see also http://tools.ietf.org/html/rfc2822#section-3.2.5
                r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
                r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$)'  # domain
                r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$',
                re.IGNORECASE)
        return object.__new__(cls, *args)

    def validate(self, email):
        if email != DEFAULT_FIELD_VALUE and email and len(email) > 6:
            if self.regex.search(email):
                return True
        return False


class EmailField(StringField):
    def validate(self, request, value):
        validation_result = super(EmailField, self).validate(request, value)

        if not validation_result.is_success:
            return validation_result

        if not EmailValidator().validate(email=value):
            return ValidationResult(
                is_success=False, reason=u"Invalid email address")

        return ValidationResult(is_success=True)
