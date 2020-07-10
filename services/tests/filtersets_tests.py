"""The filtersets tests module."""
import pytest
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from services.filtersets import _get_services

pytestmark = pytest.mark.django_db


def test_get_services(services: QuerySet):
    """Should return the filtered list of services."""
    assert not _get_services(None).count()
    request = HttpRequest()
    user = services[0].professional.user
    request.user = user
    result = _get_services(request)
    assert result.count() == 4
    assert not [r for r in result.all() if r.professional.user != user]
