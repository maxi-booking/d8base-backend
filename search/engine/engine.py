"""The search engine module."""
from typing import List

from professionals.models import Professional
from services.models import Service

from .request import SearchRequest
from .response import SearchResponse


class SearchEngine():
    """The search engine class."""

    def get(self, request: SearchRequest) -> List[SearchResponse]:
        """Return the search results."""
        # remove!!
        result = []
        for professional in Professional.objects.get_extended_list()[0:10]:
            response = SearchResponse()
            response.professional = professional
            response.services = list(
                Service.objects.get_extended_list().filter(
                    professional=professional))
            result.append(response)
        return result


def get_search_engine() -> SearchEngine:
    """Return the search engine."""
    engine = SearchEngine()
    return engine
