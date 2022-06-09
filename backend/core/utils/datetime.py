"""
Custom datetime utilities
"""
from django.utils.timezone import now


def current_year() -> int:
    return now().year
