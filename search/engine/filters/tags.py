"""The search tags filter module."""

from django.db.models import Q, QuerySet

from search.engine.request import SearchRequest

from .abstract import AbstractHandler


class TagsHandler(AbstractHandler):
    """The tags handler."""

    def _check_request(self, request: SearchRequest) -> bool:
        """Check whether the handler is applicable to the request."""
        return bool(request.tags)

    def _apply(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Apply the handler to the request."""
        return query.filter(
            Q(tags__name__in=request.tags)
            | Q(professional__tags__name__in=request.tags))
