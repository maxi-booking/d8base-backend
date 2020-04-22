"""The filtersets tests module."""
import pytest
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from professionals.filtersets import _get_professionals

pytestmark = pytest.mark.django_db


def test_get_professionals(professionals: QuerySet):
    """Should return the filtered list of professionals."""
    assert not _get_professionals(None).count()
    request = HttpRequest()
    user = professionals[0].user
    request.user = user
    result = _get_professionals(request)
    assert result.count() == 2
    assert result[0].user == professionals[0].user
