"""The search professional level filter module."""
from django.db.models import QuerySet

from search.engine.request import SearchRequest

from .abstract import AbstractHandler


class ProfessionalLevelHandler(AbstractHandler):
    """The professional level handler."""

    def _check_request(self, request: SearchRequest) -> bool:
        """Check whether the handler is applicable to the request."""
        return bool(request.professional.professional_level)

    def _apply(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Apply the handler to the request."""
        return query.filter(
            professional__level=request.professional.professional_level)
