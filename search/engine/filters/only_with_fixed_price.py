"""The search only with fixed price filter module."""

from django.db.models import QuerySet

from search.engine.request import SearchRequest

from .abstract import AbstractHandler


class OnlyWithFixedPriceHandler(AbstractHandler):
    """The only with fixed price handler."""

    def _check_request(self, request: SearchRequest) -> bool:
        """Check whether the handler is applicable to the request."""
        return bool(request.service.only_with_fixed_price)

    def _apply(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Apply the handler to the request."""
        return query.filter(price__is_price_fixed=True)
