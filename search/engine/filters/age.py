"""The search age filter module."""
import arrow
from django.db.models import QuerySet

from search.engine.request import SearchRequest

from .abstract import AbstractHandler


class AgeHandler(AbstractHandler):
    """The age handler."""

    def _check_request(self, request: SearchRequest) -> bool:
        """Check whether the handler is applicable to the request."""
        return bool(request.professional.start_age
                    or request.professional.end_age)

    def _apply(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Apply the handler to the request."""
        start = request.professional.start_age
        end = request.professional.end_age
        if start:
            start_date = arrow.utcnow().shift(years=-start).date()
            query = query.filter(professional__user__birthday__lte=start_date)
        if end:
            end_date = arrow.utcnow().shift(years=-(end + 1)).date()
            query = query.filter(professional__user__birthday__gte=end_date)
        return query
