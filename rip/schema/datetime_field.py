import datetime

from rip import datetime_converter
from rip.schema.base_field import \
    BaseField


class DateTimeField(BaseField):
    field_type = datetime.datetime

    def serialize(self, request, value):
        if value is None:
            return value
        timezone = request.context_params['timezone']
        return datetime_converter.datetime_to_timestamp(
            value, timezone=timezone)

    def clean(self, request, value):
        if value is None:
            return value
        timezone = request.context_params['timezone']
        return datetime_converter.timestamp_to_datetime(float(value), timezone)
