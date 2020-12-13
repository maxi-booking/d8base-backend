"""The search price filter module."""
from django.db.models import QuerySet

from search.engine.request import SearchRequest

from .abstract import AbstractHandler


class PriceHandler(AbstractHandler):
    """The price handler."""

    def _check_request(self, request: SearchRequest) -> bool:
        """Check whether the handler is applicable to the request."""
        return bool(request.service.start_price or request.service.end_price)

    def _apply(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Apply the handler to the request."""
        start = request.service.start_price
        end = request.service.end_price
        query = query.filter(price__is_price_fixed=True)
        if start:
            query = query.filter(
                price__price__gte=start,
                price__price_currency=start.currency,
            )
        if end:
            query = query.filter(
                price__price__lte=end,
                price__price_currency=end.currency,
            )
        return query
