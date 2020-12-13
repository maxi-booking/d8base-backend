"""The search only with auto order confirmation filter module."""

from django.db.models import QuerySet

from search.engine.request import SearchRequest

from .abstract import AbstractHandler


class OnlyWithAutoOrderConfirmationHandler(AbstractHandler):
    """The only with auto order confirmation handler."""

    def _check_request(self, request: SearchRequest) -> bool:
        """Check whether the handler is applicable to the request."""
        return bool(request.service.only_with_auto_order_confirmation)

    def _apply(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Apply the handler to the request."""
        return query.filter(is_auto_order_confirmation=True)
