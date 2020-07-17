"""The filters test module."""
import pytest
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from conftest import OBJECTS_TO_CREATE
from users.filters import OwnerFilter
from users.models import User

pytestmark = pytest.mark.django_db


class MockView():
    """The mock view class."""

    is_owner_filter_enabled = False
    owner_filter_field = "user"


def test_owner_filter_field(
    user: User,
    user_languages: QuerySet,
    professional_tags: QuerySet,
):
    """Should filter a queryset by user."""
    request = HttpRequest()
    request.user = user
    view = MockView()
    owner_filter = OwnerFilter()

    assert owner_filter.filter_queryset(
        request,
        user_languages,
        view,
    ).count() == 4

    view.is_owner_filter_enabled = True

    query = owner_filter.filter_queryset(
        request,
        user_languages,
        view,
    )
    assert query.count() == 1
    assert query[0].user == user

    del view.is_owner_filter_enabled

    assert owner_filter.filter_queryset(
        request,
        user_languages,
        view,
    ).count() == 4

    view.is_owner_filter_enabled = True
    view.owner_filter_field = "professional__user"

    assert owner_filter.filter_queryset(
        request,
        professional_tags,
        view,
    ).count() == OBJECTS_TO_CREATE * 2
