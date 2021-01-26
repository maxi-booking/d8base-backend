"""The search dates filter module."""

from django.db.models import Q, QuerySet

from search.engine.request import SearchRequest

from .abstract import AbstractHandler


class DatesHandler(AbstractHandler):
    """The dates handler."""

    # pylint: disable=inconsistent-return-statements

    def _check_request(self, request: SearchRequest) -> bool:
        """Check whether the handler is applicable to the request."""
        return bool(request.start_datetime or request.end_datetime)

    def _apply(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Apply the handler to the request."""
        start = request.start_datetime
        end = request.end_datetime
        if start and end:
            return query.filter(
                Q(
                    is_base_schedule=True,
                    professional__slots__service__isnull=True,
                    professional__slots__start_datetime__lte=end.datetime,
                    professional__slots__end_datetime__gte=start.datetime,
                ) | Q(
                    is_base_schedule=False,
                    slots__start_datetime__lte=end.datetime,
                    slots__end_datetime__gte=start.datetime,
                ))
        if start:
            return query.filter(
                Q(
                    is_base_schedule=True,
                    professional__slots__service__isnull=True,
                    professional__slots__end_datetime__gte=start.datetime,
                ) | Q(
                    is_base_schedule=False,
                    slots__end_datetime__gte=start.datetime,
                ))
        if end:
            return query.filter(
                Q(
                    is_base_schedule=True,
                    professional__slots__service__isnull=True,
                    professional__slots__start_datetime__lte=end.datetime,
                ) | Q(
                    is_base_schedule=False,
                    slots__start_datetime__lte=end.datetime,
                ))
