import re
import urlparse

from rip.schema.string_field import StringField
from rip.schema.default_field_value import DEFAULT_FIELD_VALUE
from rip.schema.validation_result import ValidationResult


class UrlValidator(object):
    regex = None

    def __new__(cls, *args):
        if cls.regex is None:
            cls.regex = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'localhost|'  #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return object.__new__(cls, *args)

    def validate(self, url):
        if url != DEFAULT_FIELD_VALUE and url:
            url = u'http://{}'.format(url) if \
                not urlparse.urlparse(url).scheme else url
            if self.regex.search(url):
                return True
        return False


class UrlField(StringField):
    def validate(self, request, value):
        validation_result = super(UrlField, self).validate(request, value)

        if not validation_result.is_success:
            return validation_result
        if self.nullable and value is None:
            return ValidationResult(is_success=True)
        if value == DEFAULT_FIELD_VALUE:
            return ValidationResult(is_success=True)
        if not self.required and not value:
            return ValidationResult(is_success=True)

        if not UrlValidator().validate(url=value):
            return ValidationResult(
                is_success=False, reason=u"The url is not valid")

        return ValidationResult(is_success=True)
