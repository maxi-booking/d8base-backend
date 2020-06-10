"""The filtersets tests module."""
import pytest
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from communication.filtersets import _get_reviews

pytestmark = pytest.mark.django_db


def test_get_reviews(reviews: QuerySet):
    """Should return the filtered list of reviews."""
    assert not _get_reviews(None).count()
    request = HttpRequest()
    user = reviews[0].professional.user
    request.user = user
    result = _get_reviews(request)
    assert result.count() == 1
    assert result[0].professional.user == reviews[0].professional.user
