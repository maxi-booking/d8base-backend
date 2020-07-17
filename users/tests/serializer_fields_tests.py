"""The users filtersets tests module."""
import pytest
from django.db.models.query import QuerySet
from django.http import HttpRequest

from users.serializer_fields import AccountUserLocationForeignKey

pytestmark = pytest.mark.django_db


def test_account_professional_foreign_key(user_locations: QuerySet):
    """Should return the filtered list of user_locations by a user."""
    obj = AccountUserLocationForeignKey()
    request = HttpRequest()
    user = user_locations[0].user
    request.user = user
    obj._context = {"request": request}  # pylint: disable=protected-access
    result = obj.get_queryset()

    assert user_locations.count() == 4
    assert result.count() == 2
    assert result.first().user == user
