"""The managers test module."""

import arrow
import pytest
from django.contrib.admin.sites import AdminSite
from django.db.models import QuerySet
from django.test.client import Client
from django.urls import reverse

from schedule.admin import AvailabilitySlotAdmin
from schedule.models import AvailabilitySlot

pytestmark = pytest.mark.django_db


def test_availability_slot_admin_weekday(professionals: QuerySet):
    """Should return a weekday for an object."""
    slot = AvailabilitySlot()
    slot.professional = professionals.first()
    now = arrow.utcnow()
    tomorrow = now.shift(days=1)
    slot.start_datetime = now.datetime
    slot.end_datetime = now.shift(hours=1).datetime
    admin = AvailabilitySlotAdmin(
        model=AvailabilitySlot,
        admin_site=AdminSite(),
    )
    assert admin.weekday(slot) == now.format("dddd")
    slot.end_datetime = tomorrow.datetime

    assert admin.weekday(
        slot) == f"{now.format('dddd')} - {tomorrow.format('dddd')}"


def test_availability_slot_admin_list_filter(
    professionals: QuerySet,
    admin_client: Client,
):
    """Should set the professional filter."""
    response = admin_client.get(
        reverse("admin:schedule_availabilityslot_changelist"))
    assert response.status_code == 200
    assert response.wsgi_request.GET.get(
        "professional__pk__exact") == professionals.first().pk
