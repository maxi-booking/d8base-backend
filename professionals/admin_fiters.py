"""The users admin filters module."""
from admin_auto_filters.filters import AutocompleteFilter


class ProfessionalFilter(AutocompleteFilter):
    """The admin professional filter."""

    title = "professional"
    field_name = "professional"
