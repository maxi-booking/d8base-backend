"""The availability generator test module."""
from dataclasses import dataclass
from datetime import datetime

import arrow
import pytest
from django.db.models import QuerySet

from schedule.availability.exceptions import AvailabilityValueError
from schedule.availability.request import Request
from schedule.availability.restrictions import (ClosedPeriodsRestriction,
                                                SlotsModifier)
from schedule.models import (AvailabilitySlot, ProfessionalClosedPeriod,
                             ServiceClosedPeriod)

pytestmark = pytest.mark.django_db

# pylint: disable=protected-access


def test_closed_periods_restriction_apply(
        professional_closed_periods: QuerySet):
    """Should apply the closed periods restriction."""
    professional = professional_closed_periods.first().professional
    restriction = ClosedPeriodsRestriction()
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    request = Request()

    request.start_datetime = start
    request.end_datetime = start.shift(days=20)

    slot1 = AvailabilitySlot()
    slot1.professional = professional
    slot1.start_datetime = start.datetime
    slot1.end_datetime = start.shift(days=1).datetime

    slot2 = AvailabilitySlot()
    slot2.professional = professional
    slot2.start_datetime = start.shift(days=6).datetime
    slot2.end_datetime = start.shift(days=7).datetime

    with pytest.raises(AvailabilityValueError) as error:
        restriction.apply()
    assert "request is not set." in str(error)

    restriction.set_request(request)

    with pytest.raises(AvailabilityValueError) as error:
        restriction.apply()
    assert "slots are not set." in str(error)

    restriction.set_slots([slot1, slot2])
    result = restriction.apply()
    assert result == [slot1]


def test_closed_periods_restriction_get_closed_periods_for_slot(
    professional_closed_periods: QuerySet,
    service_closed_periods: QuerySet,
):
    """Should lazy load closed periods for the slot."""
    professional = professional_closed_periods.first().professional
    service = service_closed_periods.first().service
    service.is_base_schedule = False

    slot = AvailabilitySlot()
    slot.professional = professional
    request = Request()
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    request.start_datetime = start
    request.end_datetime = start.shift(days=20)
    restriction = ClosedPeriodsRestriction()
    restriction.set_request(request)

    assert restriction.professionals_periods is None
    assert restriction.service_periods is None

    result = restriction._get_closed_periods_for_slot(slot)
    assert len(result) == 2
    assert isinstance(result[0], ProfessionalClosedPeriod)
    assert result == restriction.professionals_periods
    assert restriction.service_periods is None

    slot.service = service
    assert len(result) == 2
    result = restriction._get_closed_periods_for_slot(slot)
    assert isinstance(result[0], ServiceClosedPeriod)
    assert result == restriction.service_periods


def test_slots_modifier_get_processed_slots():
    """Should modify the provided slots."""

    @dataclass
    class Period():
        """The period class."""

        start_datetime: datetime
        end_datetime: datetime

    modifier = SlotsModifier()
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end = start.shift(days=10)
    period = Period(start.datetime, end.datetime)

    assert modifier.get_processed_slots([], period) == []

    # the period overlaps the entire slot
    slots = [Period(start.datetime, end.datetime)]
    assert modifier.get_processed_slots(slots, period) == []

    slots = [
        Period(
            start.datetime,
            start.shift(hours=2).datetime,
        ),
        Period(
            start.shift(hours=4).datetime,
            start.shift(hours=6).datetime,
        ),
    ]
    assert modifier.get_processed_slots(slots, period) == []

    # the period doesn't overlap with the slot
    slots = [
        Period(
            start.shift(days=1).datetime,
            start.shift(days=2).datetime,
        ),
        Period(
            start.shift(days=10).datetime,
            start.shift(days=10, hours=2).datetime,
        ),
    ]
    assert modifier.get_processed_slots(slots, period) == [
        Period(
            start.shift(days=10).datetime,
            start.shift(days=10, hours=2).datetime,
        ),
    ]

    # cut off the tail of the slot
    slots = [
        Period(
            start.shift(days=1).datetime,
            start.shift(days=2).datetime,
        ),
        Period(
            start.shift(days=9).datetime,
            start.shift(days=12, hours=2).datetime,
        ),
        Period(
            start.shift(days=20).datetime,
            start.shift(days=20, hours=2).datetime,
        ),
    ]
    assert modifier.get_processed_slots(slots, period) == [
        Period(
            start.shift(days=10).datetime,
            start.shift(days=12, hours=2).datetime,
        ),
        Period(
            start.shift(days=20).datetime,
            start.shift(days=20, hours=2).datetime,
        ),
    ]

    # cut off the head of the slot
    slots = [
        Period(
            start.shift(days=1).datetime,
            start.shift(days=2).datetime,
        ),
        Period(
            start.shift(days=-2).datetime,
            start.shift(days=2, hours=2).datetime,
        ),
    ]
    assert modifier.get_processed_slots(slots, period) == [
        Period(
            start.shift(days=-2).datetime,
            start.datetime,
        ),
    ]

    # split the slot into two slots
    slots = [
        Period(
            start.shift(days=-5).datetime,
            start.shift(days=20).datetime,
        ),
        Period(
            start.shift(days=20).datetime,
            start.shift(days=21).datetime,
        ),
    ]
    assert modifier.get_processed_slots(slots, period) == [
        Period(
            start.shift(days=-5).datetime,
            start.datetime,
        ),
        Period(
            end.datetime,
            start.shift(days=20).datetime,
        ),
        Period(
            start.shift(days=20).datetime,
            start.shift(days=21).datetime,
        ),
    ]
