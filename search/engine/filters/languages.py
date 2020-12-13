"""The search languages filter module."""
from django.db.models import QuerySet

from search.engine.request import SearchRequest

from .abstract import AbstractHandler


class LanguagesHandler(AbstractHandler):
    """The languages handler."""

    def _check_request(self, request: SearchRequest) -> bool:
        """Check whether the handler is applicable to the request."""
        return bool(request.professional.languages)

    def _apply(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Apply the handler to the request."""
        return query.filter(professional__user__languages__language__in=request
                            .professional.languages)
