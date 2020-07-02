"""The filtersets tests module."""
import pytest
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from communication.filtersets import (_get_interlocutors, _get_recipients,
                                      _get_reviews, _get_senders)

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


def test_get_recipients(messages: QuerySet):
    """Should return recipients."""
    assert not _get_recipients(None).count()
    request = HttpRequest()
    user = messages[0].sender
    request.user = user
    result = _get_recipients(request)
    assert result.count() == 1
    assert result[0] == messages[0].recipient


def test_get_senders(messages: QuerySet):
    """Should return senders."""
    assert not _get_senders(None).count()
    request = HttpRequest()
    user = messages[0].recipient
    request.user = user
    result = _get_senders(request)
    assert result.count() == 1
    assert result[0] == messages[0].sender


def test_get_interlocutors(messages: QuerySet):
    """Should return interlocutors."""
    assert not _get_interlocutors(None).count()
    request = HttpRequest()
    user = messages[0].recipient
    request.user = user
    result = _get_interlocutors(request)
    assert result.count() == 1
    assert result[0] == messages[0].sender
