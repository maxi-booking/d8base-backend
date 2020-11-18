"""The availability generator test module."""
import logging
from datetime import time

import arrow
import pytest
from _pytest.logging import LogCaptureFixture
from django.db.models.query import QuerySet
from django.utils import timezone

from schedule.availability.exceptions import AvailabilityValueError
from schedule.availability.generator import (DefaultGenerator,
                                             get_availability_generator)
from schedule.availability.request import (Request, RequestAppendProcessor,
                                           RequestYearProcessor)
from schedule.availability.restrictions import AbstractRestriction
from schedule.models import (AvailabilitySlot, ProfessionalSchedule,
                             ServiceSchedule)

pytestmark = pytest.mark.django_db

# pylint: disable=protected-access


def test_abstract_generator_set_request(
    professionals: QuerySet,
    services: QuerySet,
):
    """Should set the request."""
    request = Request()
    request.professional = professionals.first()

    generator = DefaultGenerator()
    generator.set_request(request)

    assert generator._request.professional == request.professional
    assert generator._service is None

    service = services.first()
    service.is_base_schedule = True
    service.save()
    request.service = service
    request.professional = service.professional
    generator.set_request(request)

    assert generator._request.professional == request.professional
    assert generator._service is None

    service.is_base_schedule = False
    service.save()
    request.service = service
    generator.set_request(request)

    assert generator._request.professional == request.professional
    assert generator._service is request.service


def test_abstract_generator_get(professionals: QuerySet, ):
    """Should check the request and run the _get method."""
    request = Request()
    request.professional = professionals.first()
    generator = DefaultGenerator()
    generator._get = lambda: []  # type: ignore

    with pytest.raises(AvailabilityValueError):
        generator.get()
    generator.set_request(request).get()


def test_default_generator_get_schedules(
    professional_schedules: QuerySet,
    service_schedules: QuerySet,
):
    """Should return schedules."""
    request = Request()
    professional = professional_schedules.first().professional
    request.professional = professional
    generator = DefaultGenerator()
    generator.set_request(request)

    assert generator._get_schedules(
    ) == ProfessionalSchedule.objects.get_by_days(professional)

    service = service_schedules.first().service
    service.is_base_schedule = False
    service.save()
    request.service = service
    request.professional = service.professional
    generator.set_request(request)

    assert generator._get_schedules() == ServiceSchedule.objects.get_by_days(
        service)


def test_default_generator_get_timezone(professionals: QuerySet):
    """Should generate the availability slots for a different timezone."""
    zone = "America/New_York"
    professional = professionals.first()
    timezone.activate(zone)
    schedule = ProfessionalSchedule()
    schedule.professional = professional
    schedule.day_of_week = arrow.utcnow().weekday()
    schedule.start_time = time(14)
    schedule.end_time = time(23, 59)
    schedule.save()

    schedule.id = None
    schedule.day_of_week = arrow.utcnow().shift(days=1).weekday()
    schedule.start_time = time(0)
    schedule.end_time = time(10)
    schedule.save()
    timezone.activate("UTC")

    generator = DefaultGenerator()
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end = start.shift(days=13)
    request = Request()
    request.professional = professional
    request.start_datetime = start
    request.end_datetime = end
    generator.set_request(request)

    slots = generator.get()
    assert len(slots) == 2

    expected = start.replace(tzinfo=zone, hour=14, minute=0).to("UTC")
    assert slots[0].start_datetime == expected.datetime

    expected = start.shift(days=1).replace(tzinfo=zone, hour=10,
                                           minute=0).to("UTC")
    assert slots[0].end_datetime == expected.datetime


def test_default_generator_get_professional(professional_schedules: QuerySet):
    """Should generate the availability slots."""
    generator = DefaultGenerator()
    professional = professional_schedules.first().professional
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    start = start.shift(days=-start.weekday())
    end = start.shift(days=7)
    request = Request()
    request.professional = professional
    request.start_datetime = start
    request.end_datetime = end
    generator.set_request(request)

    slots = generator.get()
    assert len(slots) == 6 * 2
    assert slots[0].professional == professional
    assert slots[0].start_datetime.utcoffset().total_seconds() == 0

    expected = start.replace(hour=9)
    assert slots[0].start_datetime == expected.datetime

    expected = start.replace(hour=14)
    assert slots[0].end_datetime == expected.datetime

    expected = start.replace(hour=15)
    assert slots[1].start_datetime == expected.datetime

    expected = start.replace(hour=18)
    assert slots[1].end_datetime == expected.datetime

    expected = start.replace(hour=9).shift(days=1)
    assert slots[2].start_datetime == expected.datetime


def test_default_generator_get_service(service_schedules: QuerySet):
    """Should generate the availability slots for a service."""
    generator = DefaultGenerator()
    service = service_schedules.first().service
    service.is_base_schedule = False
    service.save()
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    start = start.shift(days=-start.weekday())
    end = start.shift(days=7)
    request = Request()
    request.professional = service.professional
    request.service = service
    request.start_datetime = start
    request.end_datetime = end
    generator.set_request(request)
    slots = generator.get()

    assert len(slots) == 6 * 2
    assert slots[0].professional == service.professional
    assert slots[0].service == service
    assert slots[0].start_datetime.utcoffset().total_seconds() == 0


def test_default_generator_combine_adjacent_slots():
    """Should combine the adjacent slots."""
    # pylint: disable=too-many-statements
    slot1 = AvailabilitySlot()
    now = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    slot1.start_datetime = now
    slot1.end_datetime = slot1.start_datetime.shift(hours=3)

    slot2 = AvailabilitySlot()
    slot2.start_datetime = slot1.end_datetime.shift(hours=1)
    slot2.end_datetime = slot2.start_datetime.shift(hours=1)

    slot3 = AvailabilitySlot()
    slot3.start_datetime = slot2.end_datetime.shift(hours=1)
    slot3.end_datetime = slot3.start_datetime.shift(hours=1)

    result = DefaultGenerator._combine_adjacent_slots([slot1, slot2, slot3])
    assert len(result) == 3
    assert result[0] == slot1
    assert result[1] == slot2

    slot2 = AvailabilitySlot()
    slot2.start_datetime = slot1.end_datetime.shift(seconds=60)
    slot2.end_datetime = slot2.start_datetime.shift(hours=1).replace(minute=0)

    slot3 = AvailabilitySlot()
    slot3.start_datetime = slot2.end_datetime.shift(hours=1)
    slot3.end_datetime = slot3.start_datetime.shift(hours=1)

    result = DefaultGenerator._combine_adjacent_slots([slot1, slot2, slot3])
    assert len(result) == 2
    assert result[1] == slot3
    assert result[0].start_datetime == now
    assert result[0].end_datetime == now.shift(hours=4)

    slot2 = AvailabilitySlot()
    slot2.start_datetime = slot1.end_datetime.shift(seconds=1)
    slot2.end_datetime = slot2.start_datetime.shift(hours=1)

    slot3 = AvailabilitySlot()
    slot3.start_datetime = slot2.end_datetime.shift(seconds=1)
    slot3.end_datetime = slot3.start_datetime.shift(hours=1)

    slot4 = AvailabilitySlot()
    slot4.start_datetime = slot3.end_datetime.shift(seconds=1)
    slot4.end_datetime = slot4.start_datetime.shift(hours=1)

    slot5 = AvailabilitySlot()
    slot5.start_datetime = slot4.end_datetime.shift(seconds=1)
    slot5.end_datetime = slot5.start_datetime.shift(hours=1)

    result = DefaultGenerator._combine_adjacent_slots([
        slot1,
        slot2,
        slot3,
        slot4,
        slot5,
    ])
    assert len(result) == 1
    assert result[0].start_datetime == slot1.start_datetime
    assert result[0].end_datetime == slot5.end_datetime

    result = DefaultGenerator._combine_adjacent_slots([
        slot1,
        slot2,
    ])
    assert len(result) == 1
    assert result[0].start_datetime == slot1.start_datetime
    assert result[0].end_datetime == slot2.end_datetime

    result = DefaultGenerator._combine_adjacent_slots([slot1])
    assert len(result) == 1
    assert result[0] == slot1

    slot3 = AvailabilitySlot()
    slot3.start_datetime = slot2.end_datetime.shift(hours=1)
    slot3.end_datetime = slot3.start_datetime.shift(hours=1)

    slot4 = AvailabilitySlot()
    slot4.start_datetime = slot3.end_datetime.shift(seconds=1)
    slot4.end_datetime = slot4.start_datetime.shift(hours=1)

    slot5 = AvailabilitySlot()
    slot5.start_datetime = slot4.end_datetime.shift(seconds=1)
    slot5.end_datetime = slot5.start_datetime.shift(hours=1)

    result = DefaultGenerator._combine_adjacent_slots([
        slot1,
        slot2,
        slot3,
        slot4,
        slot5,
    ])
    assert len(result) == 2
    assert result[0].start_datetime == slot1.start_datetime
    assert result[0].end_datetime == slot2.end_datetime
    assert result[1].start_datetime == slot3.start_datetime
    assert result[1].end_datetime == slot5.end_datetime

    assert DefaultGenerator._combine_adjacent_slots([]) == []


def test_availability_get_generator(
    professional_schedules: QuerySet,
    caplog: LogCaptureFixture,
):
    """Should set dates and a professional."""
    request = Request()
    request.professional = professional_schedules.first().professional
    generator = get_availability_generator(request)

    assert isinstance(generator.logger, logging.Logger)
    assert isinstance(generator.request_processor, RequestYearProcessor)

    request.append_days = True
    generator = get_availability_generator(request)

    assert isinstance(generator.logger, logging.Logger)
    assert isinstance(generator.request_processor, RequestAppendProcessor)

    caplog.clear()
    AvailabilitySlot.objects.all().delete()
    assert AvailabilitySlot.objects.all().count() == 0
    generator.generate()
    assert "AvailabilityGenerator report: request" in caplog.records[0].message
    assert AvailabilitySlot.objects.all().count() > 0


def test_availability_generator_exception(
    professionals: QuerySet,
    caplog: LogCaptureFixture,
):
    """Should raise an exception."""

    def mock(request: Request):
        """Raise an exception."""
        raise AvailabilityValueError()

    caplog.clear()
    request = Request()
    request.professional = professionals.first()
    generator = get_availability_generator(request)
    generator.request_processor.get = mock  # type: ignore
    generator.generate()
    assert "AvailabilityGenerator error" in caplog.records[0].message


def test_availability_generator_apply_restrictions():
    """Should apply the restrictions to the slots."""

    class RestrictionOne(AbstractRestriction):
        """The mock class."""

        def _apply(self):
            """Apply the restriction to the availability slots."""
            return [2, 3, 4]

    class RestrictionTwo(AbstractRestriction):
        """The mock class."""

        def _apply(self):
            """Apply the restriction to the availability slots."""
            return [5, 6, 7]

    request = Request()
    generator = get_availability_generator(request)
    generator.restrictions = [RestrictionOne()]
    slots = generator._apply_restrictions([1, 2, 3])  # type: ignore

    assert slots == [2, 3, 4]

    generator.restrictions = [RestrictionOne(), RestrictionTwo()]
    slots = generator._apply_restrictions([1, 2, 3])  # type: ignore

    assert slots == [5, 6, 7]
