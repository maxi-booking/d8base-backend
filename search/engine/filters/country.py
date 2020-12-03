"""The search country filter module."""

from django.db.models import QuerySet

from search.engine.request import SearchRequest

from .abstract import AbstractHandler


class CountryHandler(AbstractHandler):
    """The country handler."""

    def _check_request(self, request: SearchRequest) -> bool:
        """Check whether the handler is applicable to the request."""
        return bool(request.location.country)

    def _apply(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Apply the handler to the request."""
        return query.filter(
            locations__location__country=request.location.country)
