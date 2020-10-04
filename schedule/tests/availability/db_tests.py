"""The availability db test module."""
import arrow
import pytest
from django.db.models.query import QuerySet

from schedule.availability.db import DeleteSaver
from schedule.availability.exceptions import AvailabilityValueError
from schedule.availability.request import Request, RequestYearProcessor
from schedule.models import AvailabilitySlot

pytestmark = pytest.mark.django_db

# pylint: disable=protected-access


def test_abstract_saver_set_request_slots(
    professionals: QuerySet,
    availability_slots: QuerySet,
):
    """Should set the request slots."""
    request = Request()
    request.professional = professionals.first()

    saver = DeleteSaver()
    with pytest.raises(AvailabilityValueError) as error:
        saver._check_request()
    assert "request is not set" in str(error)

    saver.set_request(request)
    with pytest.raises(AvailabilityValueError) as error:
        saver._check_request()
    assert "slots are not set" in str(error)

    saver.set_slots(list(availability_slots))
    saver._check_request()
    assert saver._request == request
    assert saver._slots == list(availability_slots)


def test_delete_saver_save(professionals: QuerySet):
    """Should save the provided slots."""
    start = arrow.utcnow()
    end = start.shift(hours=3)
    professional = professionals.first()
    slot = AvailabilitySlot()
    slot.professional = professional
    slot.start_datetime = start.datetime
    slot.end_datetime = end.datetime
    slot.save()

    pk = slot.pk
    slot.pk = None

    request = Request()
    request.professional = professionals.first()
    request = RequestYearProcessor().get(request)

    saver = DeleteSaver()
    saver.set_request(request).set_slots([slot])
    saver.save()

    slots = AvailabilitySlot.objects.all()
    assert slots.count() == 1
    assert slot.pk != pk

    assert saver.set_slots([]).save() is None  # type: ignore
