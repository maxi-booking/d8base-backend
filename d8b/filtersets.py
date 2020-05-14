"""The d8b filtersets module."""
from django_filters import rest_framework as filters


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    """The number in filter class."""
