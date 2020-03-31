"""The fields tests module."""
from django.conf import settings
from pytz import common_timezones

from d8b.fields import LanguageField, TimezoneField, UnitsField


def test_language_field():
    """Should create a language field."""
    field = LanguageField()
    assert field.max_length == 2
    assert field.choices == settings.LANGUAGES


def test_timezone_field():
    """Should create a timezone field."""
    field = TimezoneField()
    assert field.max_length == 50
    assert field.choices == list(zip(common_timezones, common_timezones))


def test_units_field():
    """Should create a units field."""
    field = UnitsField()
    assert field.choices[0] == (0, 'metric')
    assert field.choices[1] == (1, 'imperial/US')
    assert field.default == 0
