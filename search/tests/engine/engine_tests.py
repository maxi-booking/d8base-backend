"""The search engine tests module."""
import pytest
from django.db.models.query import QuerySet

from d8b.settings import get_settings
from search.engine import get_search_engine
from search.engine.engine import SearchEngine
from search.engine.request import SearchRequest

pytestmark = pytest.mark.django_db
# pylint: disable=protected-access


def test_get_search_engine():
    """Must return a search engine object."""
    assert isinstance(get_search_engine(), SearchEngine)


def test_engine_set_offset_and_limit():
    """Must set the offset and limit."""
    page_size = get_settings("D8B_SEARCH_PAGE_SIZE")
    request = SearchRequest()
    request.page = 1
    engine = get_search_engine()
    engine.request = request
    engine.set_offset_and_limit()

    assert engine.offset == 0
    assert engine.limit == page_size

    engine.request.page = 2
    engine.set_offset_and_limit()

    assert engine.offset == page_size
    assert engine.limit == page_size * 2

    engine.request.page = 5
    engine.set_offset_and_limit()

    assert engine.offset == page_size * 4
    assert engine.limit == page_size * 5


def test_engine_get_services_ids(services: QuerySet):
    """Must return services ids."""
    request = SearchRequest()
    request.page = 1
    engine = get_search_engine()
    engine.request = request
    engine.set_offset_and_limit()
    ids = engine._get_services_ids()
    assert len(ids) == services.filter(is_enabled=True).count()


def test_engine_get_professionals(services: QuerySet):
    """Must return professionals."""
    request = SearchRequest()
    request.page = 1
    engine = get_search_engine()
    engine.request = request
    engine.set_offset_and_limit()
    ids = engine._get_services_ids()
    professionals = engine._get_professionals(ids)

    assert professionals.count() == len(
        services.filter(is_enabled=True).values_list("professional__pk"))


def test_engine_get_professional_services(services: QuerySet):
    """Must return professionals."""
    professional = services.first().professional
    engine = get_search_engine()

    assert not engine._get_professional_services(professional, [])
    assert not engine._get_professional_services(professional, [0, -1])
    assert len(
        engine._get_professional_services(
            professional,
            [services.first().pk],
        )) == 1
    query = services.filter(professional=professional)
    assert len(
        engine._get_professional_services(
            professional,
            query.values_list("pk"),
        )) == query.count()


def test_engine_get(services: QuerySet, elasticsearch_setup: None):
    """Must return search results."""
    # pylint: disable=unused-argument
    request = SearchRequest()
    request.page = 1
    engine = get_search_engine()
    _, count = engine.get(request)

    assert count == services.filter(
        is_enabled=True).values_list("professional__pk").count()

    service = services.filter(is_enabled=True).first()
    service.name = "rather peculiar name"
    service.save()
    request.query = service.name
    _, count = engine.get(request)

    assert count == 1
