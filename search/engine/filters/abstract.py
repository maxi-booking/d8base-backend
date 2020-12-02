"""The search abstract filter module."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from django.db.models import QuerySet

from search.engine.request import SearchRequest


class Handler(ABC):
    """The handler interface."""

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        """Set the next handler."""

    @abstractmethod
    def _check_request(self, request: SearchRequest) -> bool:
        """Check whether the handler is applicable to the request."""

    @abstractmethod
    def _apply(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Apply the handler to the request."""

    @abstractmethod
    def handle(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Run the handler."""


class AbstractHandler(Handler):
    """The default handler interface."""

    _next_handler: Optional[Handler] = None

    def set_next(self, handler: Handler) -> Handler:
        """Set the next handler."""
        self._next_handler = handler
        return handler

    def handle(self, request: SearchRequest, query: QuerySet) -> QuerySet:
        """Run the handler."""
        if self._check_request(request):
            query = self._apply(request, query)
        if self._next_handler:
            return self._next_handler.handle(request, query)
        return query
