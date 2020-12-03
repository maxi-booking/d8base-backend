"""The search district filter module."""

from django.db.models import QuerySet

from search.engine.request import SearchRequest

from .abstract import AbstractHandler


class DistrictHandler(AbstractHandler):
    """The district handler."""

    def _check_request(self, request: SearchRequest) -> bool:
        """Check whether the handler is applicable to the request."""
        return bool(request.location.district)

    def _apply(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Apply the handler to the request."""
        return query.filter(
            locations__location__district=request.location.district)
