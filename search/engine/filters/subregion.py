"""The search subregion filter module."""

from django.db.models import QuerySet

from search.engine.request import SearchRequest

from .abstract import AbstractHandler


class SubregionHandler(AbstractHandler):
    """The subregion handler."""

    def _check_request(self, request: SearchRequest) -> bool:
        """Check whether the handler is applicable to the request."""
        return bool(request.location.subregion)

    def _apply(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Apply the handler to the request."""
        return query.filter(
            locations__location__subregion=request.location.subregion)
