"""The communication admin filters module."""
from admin_auto_filters.filters import AutocompleteFilter


class SenderFilter(AutocompleteFilter):
    """The admin sender filter."""

    title = 'sender'
    field_name = 'sender'


class RecipientFilter(AutocompleteFilter):
    """The admin recipient filter."""

    title = 'recipient'
    field_name = 'recipient'
