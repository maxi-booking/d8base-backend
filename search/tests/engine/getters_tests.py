"""The search engine getters tests module."""
import pytest
from django.db.models.query import QuerySet
from pytest_mock import MockFixture

from search.engine.getters import ServiceSearchGetter
from search.engine.request import SearchRequest

pytestmark = pytest.mark.django_db
# pylint: disable=protected-access


def test_getter_get_filters():
    """Must return the getter filters."""
    getter = ServiceSearchGetter()
    current_filter = getter._get_filters()
    count = 0
    while current_filter._next_handler:
        current_filter = current_filter._next_handler
        count += 1

    assert count == 24


def test_getter_get_base_query(services: QuerySet):
    """Must return the base query."""
    request = SearchRequest()
    getter = ServiceSearchGetter()
    getter.request = request

    assert getter._get_base_query().count() == services.filter(
        is_enabled=True).count()

    getter.request.query = "invalid query"
    assert not getter._get_base_query().count()


def test_getter_get_query(
    services: QuerySet,
    mocker: MockFixture,
):
    """Must return the base query."""
    request = SearchRequest()
    getter = ServiceSearchGetter()

    assert getter.get_query(request).count() == services.filter(
        is_enabled=True).count()

    country = mocker.patch("search.engine.filters.PriceHandler.handle")
    assert getter.get_query(request)
    country.assert_called_once()
