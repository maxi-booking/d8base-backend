"""The search engine validators module."""

from typing import TYPE_CHECKING

# from .exceptions import SearchValidationError

if TYPE_CHECKING:
    from .request import SearchRequest


def validate_search_request(request: "SearchRequest"):
    """Validate the calendar request."""
    # raise SearchValidationError("test")
