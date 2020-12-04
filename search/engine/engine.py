"""The search engine module."""
from abc import ABC, abstractmethod
from typing import List, Tuple

from django.db.models.query import QuerySet
from django.utils.module_loading import import_string

from d8b.settings import get_settings
from professionals.models import Professional
from services.models import Service

from .getters import AbstractSearchGetter, ServiceSearchGetter
from .request import SearchRequest
from .response import SearchResponse


class AbstractSearchEngine(ABC):
    """The abstract search engine class."""

    @abstractmethod
    def get(self, request: SearchRequest) -> Tuple[List[SearchResponse], int]:
        """Return the search results."""


class SearchEngine(AbstractSearchEngine):
    """The search engine class."""

    request: SearchRequest
    services_getter: AbstractSearchGetter = ServiceSearchGetter()
    page_size: int = get_settings("D8B_SEARCH_PAGE_SIZE")
    offset: int = 0
    limit: int = page_size

    def _get_services_ids(self) -> QuerySet:
        """Get the services ids."""
        return list(
            self.services_getter.get_query(self.request).values_list(
                "pk",
                flat=True,
            )[:get_settings("D8B_SEARCH_MAX_ENTRIES")])

    def _get_professionals(self, services_ids: QuerySet) -> QuerySet:
        """Get the professionals."""
        ids = Service.objects.filter(pk__in=services_ids).values_list(
            "professional__pk", flat=True)[self.offset:self.limit]
        return Professional.objects.get_extended_list().filter(pk__in=ids)

    @staticmethod
    def _get_professional_services(
        professional: Professional,
        ids: List[int],
    ) -> List[Service]:
        """Get the professionals."""
        return list(Service.objects.get_extended_list().filter(
            professional=professional,
            pk__in=ids,
        ))

    def set_offset_and_limit(self):
        """Set the offset and limit for the queries."""
        if self.request.page > 1:
            self.offset = self.page_size * (self.request.page - 1)
        self.limit = self.offset + self.page_size

    def get(self, request: SearchRequest) -> Tuple[List[SearchResponse], int]:
        """Return the search results."""
        self.request = request
        self.set_offset_and_limit()
        service_ids = self._get_services_ids()

        result = []
        for professional in self._get_professionals(service_ids):
            response = SearchResponse()
            response.professional = professional
            response.services = self._get_professional_services(
                professional=professional,
                ids=service_ids,
            )
            result.append(response)
        return result, len(service_ids)


def get_search_engine() -> SearchEngine:
    """Return the search engine."""
    engine = import_string(get_settings("D8B_SEARCH_ENGINE_CLASS"))()
    return engine
