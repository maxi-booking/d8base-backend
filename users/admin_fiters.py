"""The users admin filters module."""
from admin_auto_filters.filters import AutocompleteFilter


class UserFilter(AutocompleteFilter):
    """The admin user filter."""

    title = 'user'
    field_name = 'user'
