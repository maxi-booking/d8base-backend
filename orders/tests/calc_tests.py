"""The services test module."""

import pytest
from django.db.models import QuerySet
from djmoney.money import Money

from orders.calc import Calculator
from orders.models import Order

pytestmark = pytest.mark.django_db


def test_calculator_calc(services: QuerySet):
    """Should calc the order price."""
    order = Order()
    calc = Calculator()
    assert calc.calc(order) is None

    service = services.first()
    service.price.is_price_fixed = False
    order.service = service

    assert calc.calc(order) is None

    service.price.is_price_fixed = True
    service.price.price = Money(1, "USD")

    assert calc.calc(order) == service.price.price
