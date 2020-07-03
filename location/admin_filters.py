"""The location admin filters module."""
from admin_auto_filters.filters import AutocompleteFilter


class RegionFilter(AutocompleteFilter):
    """The admin region filter."""

    title = 'region'
    field_name = 'region'


class CityFilter(AutocompleteFilter):
    """The admin city filter."""

    title = 'city'
    field_name = 'city'


class DistrictFilter(AutocompleteFilter):
    """The admin district filter."""

    title = 'district'
    field_name = 'district'
