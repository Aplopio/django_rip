import calendar
import datetime
import pytz

def datetime_to_timestamp(_date, timezone):
    if not hasattr(_date, "tzinfo"):
        _date = datetime.datetime.combine(_date, datetime.time())
    return calendar.timegm(pytz.timezone(timezone).localize(_date).astimezone(
        pytz.UTC).utctimetuple())


def timestamp_to_datetime(timestamp, timezone):
    tz = pytz.timezone(timezone)
    tz_aware_datetime = datetime.datetime.fromtimestamp(timestamp, tz=tz)
    return tz_aware_datetime.replace(tzinfo=None)
