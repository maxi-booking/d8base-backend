"""The location services test module."""
from typing import List

import pytest
from cities.models import (City, Country, District, PostalCode, Region,
                           Subregion)

from location.interfaces import AbstractLocation
from professionals.services import LocationCopyAutofiller

pytestmark = pytest.mark.django_db


def test_location_autofiller_set_from_region(
    countries: List[Country],
    regions: List[Region],
    subregions: List[Subregion],
    cities: List[City],
    districts: List[District],
    postal_codes: List[PostalCode],
):
    """Should autofill location from a region."""
    source = AbstractLocation()
    source.country = countries[1]
    source.region = regions[0]
    source.subregion = subregions[0]
    source.city = cities[1]
    source.district = districts[0]
    source.postal_code = postal_codes[1]
    source.address = 'test address'
    source.units = 1
    source.timezone = 'test timezone'
    destination = AbstractLocation()
    LocationCopyAutofiller(destination, source).autofill_location()

    assert destination.country == source.country
    assert destination.region == source.region
    assert destination.subregion == source.subregion
    assert destination.city == source.city
    assert destination.district == source.district
    assert destination.postal_code == source.postal_code
    assert destination.address == source.address
    assert destination.units == source.units
    assert destination.timezone == source.timezone
