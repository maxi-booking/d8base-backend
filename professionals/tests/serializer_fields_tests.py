"""The filtersets tests module."""
import pytest
from django.db.models.query import QuerySet
from django.http import HttpRequest

from professionals.serializer_fields import AccountProfessionalForeignKey

pytestmark = pytest.mark.django_db


def test_account_professional_foreign_key(professionals: QuerySet):
    """Should return the filtered list of professionals by a user."""
    obj = AccountProfessionalForeignKey()
    request = HttpRequest()
    user = professionals[0].user
    request.user = user
    obj._context = {"request": request}  # pylint: disable=protected-access
    result = obj.get_queryset()

    assert professionals.count() == 4
    assert result.count() == 2
    assert result.first().user == user
