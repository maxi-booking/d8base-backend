"""The services validators test module."""

import pytest
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from moneyed import EUR, USD, Money

from services.models import Service
from services.validators import (validate_service_location,
                                 validate_service_price)

pytestmark = pytest.mark.django_db


def test_validate_service_price(services: QuerySet):
    """Should validate a service price."""
    price = services.first().price
    price.is_price_fixed = True
    price.price = None
    with pytest.raises(ValidationError):
        validate_service_price(price)

    price.price = Money(0.34, EUR)
    validate_service_price(price)

    price.is_price_fixed = False
    price.start_price = None
    with pytest.raises(ValidationError):
        validate_service_price(price)

    price.start_price = Money(0.34, EUR)
    price.end_price = Money(1.5, USD)
    with pytest.raises(ValidationError):
        validate_service_price(price)

    price.start_price = Money(2.5, USD)
    with pytest.raises(ValidationError):
        validate_service_price(price)

    price.start_price = Money(0.5, USD)
    validate_service_price(price)


def test_validate_service_location(
    services: QuerySet,
    professionals: QuerySet,
):
    """Should validate a service location."""
    location = services.filter(
        service_type=Service.TYPE_CLIENT_LOCATION).first().locations.first()
    validate_service_location(location)
    location.service.professional = professionals.exclude(
        pk=location.location.professional.pk).first()

    with pytest.raises(ValidationError):
        validate_service_location(location)
