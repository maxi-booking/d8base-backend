"""The orders fixtures module."""

import arrow
import pytest
from django.db.models.query import QuerySet
from djmoney.money import Money

from orders.models import Order

# pylint: disable=redefined-outer-name


@pytest.fixture
def orders(
    users: QuerySet,
    professionals: QuerySet,
    services: QuerySet,
) -> "QuerySet[Order]":
    """Return a services queryset."""
    # pylint: disable=unused-argument
    user = users.first()
    for professional in professionals.distinct("user").order_by("user"):
        service = professional.services.first()
        order = Order()
        order.client = user
        order.start_datetime = arrow.utcnow().shift(hours=2).datetime
        order.end_datetime = arrow.utcnow().shift(hours=4).datetime
        order.service = service
        order.note = f"note {service.pk}"
        order.remind_before = 60
        order.price = Money(10, "USD")
        order.save()

        service = professional.services.last()
        order = Order()
        order.client = user
        order.start_datetime = arrow.utcnow().shift(hours=6, days=1).datetime
        order.end_datetime = arrow.utcnow().shift(hours=10, days=1).datetime
        order.service = service
        order.note = f"note {service.pk}"
        order.save()
    return Order.objects.get_list()
