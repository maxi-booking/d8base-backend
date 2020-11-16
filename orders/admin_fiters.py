"""The orders admin filters module."""
from admin_auto_filters.filters import AutocompleteFilter


class ClientFilter(AutocompleteFilter):
    """The admin client filter."""

    title = "client"
    field_name = "client"


class ServiceFilter(AutocompleteFilter):
    """The admin service filter."""

    title = "service"
    field_name = "service"
