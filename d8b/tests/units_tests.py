"""The units tests module."""
from decimal import Decimal
from typing import Optional

import pytest
from django.conf import settings
from django.utils import timezone

from d8b import units
from users.models import User, UserSettings

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("value,expected", [
    (Decimal("1"), Decimal("0.6")),
    (Decimal("0.5"), Decimal("0.3")),
    (Decimal("22.5"), Decimal("14.0")),
])
def test_convert_distance(value: Decimal, expected: Decimal):
    """Should convert a km distance to a mi distance."""
    assert units.convert_km_mi(value).quantize(Decimal(".1")) == expected
    assert units.convert_mi_km(expected).quantize(Decimal(".1")) == value


@pytest.mark.parametrize("value,expected", [
    ("Europe/Moscow", "ru"),
    ("America/New_York", "us"),
    ("America/Toronto", "ca"),
    ("Europe/London", "gb"),
    ("UTC", None),
    ("invalid", None),
])
def test_county_code_from_timezone(value: str, expected: Optional[str]):
    """Should return a country code from the provided timezone."""
    assert units.get_country_code_from_timezone(value) == expected


def test_units_from_timezone():
    """Should return units from the current timezone."""
    timezone.deactivate()

    assert units.get_units_from_timezone() == settings.UNITS_METRIC

    timezone.activate("Europe/London")
    assert units.get_units_from_timezone() == settings.UNITS_METRIC

    timezone.activate("America/New_York")
    assert units.get_units_from_timezone() == settings.UNITS_IMPERIAL

    timezone.activate("America/Toronto")
    assert units.get_units_from_timezone() == settings.UNITS_METRIC

    timezone.activate("America/Los_Angeles")
    assert units.get_units_from_timezone() == settings.UNITS_IMPERIAL

    timezone.deactivate()


def test_is_imperial_units(user: User):
    """Should return units from the current timezone."""
    assert not units.is_imperial_units(user)

    UserSettings.objects.create(user=user, units=settings.UNITS_IMPERIAL)
    user.refresh_from_db()
    assert units.is_imperial_units(user)

    UserSettings.objects.all().delete()
    user.refresh_from_db()
    assert not units.is_imperial_units(user)
