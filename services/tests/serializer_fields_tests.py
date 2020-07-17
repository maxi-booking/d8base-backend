"""The serializer fields tests module."""
import pytest
from django.db.models.query import QuerySet
from django.http import HttpRequest

from services.serializer_fields import (AccountProfessionalLocationForeignKey,
                                        AccountServiceForeignKey)

pytestmark = pytest.mark.django_db


def test_account_professional_location_foreign_key(
        professional_locations: QuerySet):
    """Should return the filtered list of professional locations by a user."""
    obj = AccountProfessionalLocationForeignKey()
    request = HttpRequest()
    user = professional_locations[0].professional.user
    request.user = user
    obj._context = {"request": request}  # pylint: disable=protected-access
    result = obj.get_queryset()

    assert professional_locations.count() == 8
    assert result.count() == 4
    assert not [r for r in result.all() if r.professional.user != user]


def test_account_service_foreign_key(services: QuerySet):
    """Should return the filtered list of services by a user."""
    obj = AccountServiceForeignKey()
    request = HttpRequest()
    user = services[0].professional.user
    request.user = user
    obj._context = {"request": request}  # pylint: disable=protected-access
    result = obj.get_queryset()

    assert services.count() == 8
    assert result.count() == 4
    assert not [r for r in result.all() if r.professional.user != user]
