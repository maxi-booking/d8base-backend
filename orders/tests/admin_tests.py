"""The admin test module."""

import pytest
from django.contrib.admin.sites import AdminSite

from orders.admin import OrderAdmin
from orders.models import Order

pytestmark = pytest.mark.django_db


def test_order_admin_get_form():
    """Should return the admin form."""
    admin = OrderAdmin(
        model=Order,
        admin_site=AdminSite(),
    )
    result = admin.get_form(None)
    assert not result.base_fields["end_datetime"].required
