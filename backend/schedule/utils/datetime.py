from datetime import datetime
from typing import Optional

from django.utils.timezone import make_aware


def combine(date: str, time: str, formats: Optional[dict] = None):
    """Combine a date string and a time string with the given formats to
    a timezone-aware datetime object that can be safely committed to the
    database.

    The formats dictionary must contain a format string for the date and for
    the time arguments. It defaults to '%Y-%m-%d' and '%H:%M', respectively.
    """
    formats = formats or {
        'date': '%Y-%m-%d',
        'time': '%H:%M'
    }

    date = datetime.strptime(date, formats['date'])
    time = datetime.strptime(time, formats['time']).time()

    date_time_combined = datetime.combine(date, time)
    return make_aware(date_time_combined)
