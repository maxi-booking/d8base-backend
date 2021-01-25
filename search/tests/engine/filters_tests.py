"""The search engine filters tests module."""

from typing import List

import pytest
from cities.models import Country, Region
from django.db.models.query import QuerySet

from search.engine import filters
from search.engine.request import SearchRequest

pytestmark = pytest.mark.django_db
# pylint: disable=protected-access,redefined-outer-name


def test_country_filter(services: QuerySet, countries: List[Country]):
    """Should filter the query."""
    services.update(is_enabled=True)
    request = SearchRequest()
    handler = filters.CountryHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.location.country = countries[1]
    assert handler.handle(request, services).count() == 0

    request.location.country = countries[0]
    assert handler.handle(request, services).count() > 1


def test_region_filter(services: QuerySet, regions: List[Region]):
    """Should filter the query."""
    services.update(is_enabled=True)
    request = SearchRequest()
    handler = filters.RegionHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.location.region = regions[1]
    assert handler.handle(request, services).count() == 0

    request.location.region = regions[0]
    assert handler.handle(request, services).count() > 1
