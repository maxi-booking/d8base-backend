"""The search exceptions module."""


class SearchError(Exception):
    """The search base error."""


class SearchValueError(SearchError):
    """The search value error."""


class SearchValidationError(SearchError):
    """The search validation error."""
