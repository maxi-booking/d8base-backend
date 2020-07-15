"""The d8b units module."""

from decimal import Decimal
from typing import TYPE_CHECKING, Dict, Optional

from django.conf import settings
from django.contrib.gis.measure import Distance
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from pytz import country_timezones

if TYPE_CHECKING:
    from users.models import User


def convert_km_mi(value: Decimal) -> Decimal:
    """Convert the km distance to mi."""
    dist = Distance(km=value)
    return Decimal(dist.mi)


def convert_mi_km(value: Decimal) -> Decimal:
    """Convert the mi distance to km."""
    dist = Distance(mi=value)
    return Decimal(dist.km)


def is_imperial_units(user: 'User') -> bool:
    """Check the request user units."""
    units = None
    if user.is_authenticated:
        try:
            units = user.settings.units
        except ObjectDoesNotExist:
            pass
    if units is None:
        units = get_units_from_timezone()
    return units == settings.UNITS_IMPERIAL


def get_country_code_from_timezone(name: str) -> Optional[str]:
    """Return a country code based on the timezone."""
    timezone_country: Dict[str, str] = {}
    for countrycode in country_timezones:
        timezones = country_timezones[countrycode]
        for val in timezones:
            timezone_country[val] = countrycode
    result = timezone_country.get(name, '').lower()
    return result or None


def get_units_from_timezone() -> int:
    """Get units from the current timezone."""
    name = timezone.get_current_timezone_name()
    code = get_country_code_from_timezone(name)
    if code and code in settings.IMPERIAL_UNITS_COUNTRIES:
        return settings.UNITS_IMPERIAL
    return settings.UNITS_METRIC
