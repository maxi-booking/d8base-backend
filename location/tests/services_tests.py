"""The location services test module."""
from typing import List

import pytest
from cities.models import (City, Country, District, PostalCode, Region,
                           Subregion)

from location.interfaces import AbstractLocation
from location.services import LocationAutofiller

pytestmark = pytest.mark.django_db


def test_location_autofiller_set_from_region(
    countries: List[Country],
    regions: List[Region],
):
    """Should autofill location from a region."""
    location = AbstractLocation()
    location.country = countries[1]
    location.region = regions[0]
    LocationAutofiller(location).autofill_location()

    assert location.region == regions[0]
    assert location.country == regions[0].country


def test_location_autofiller_set_from_subregion(
    countries: List[Country],
    subregions: List[Subregion],
):
    """Should autofill location from a subregion."""
    location = AbstractLocation()
    location.country = countries[1]
    location.subregion = subregions[0]
    LocationAutofiller(location).autofill_location()

    assert location.subregion == subregions[0]
    assert location.region == subregions[0].region
    assert location.country == subregions[0].region.country


def test_location_autofiller_set_from_city(
    regions: List[Region],
    cities: List[City],
):
    """Should autofill location from a city."""
    location = AbstractLocation()
    location.region = regions[1]
    location.city = cities[0]
    LocationAutofiller(location).autofill_location()

    assert location.city == cities[0]
    assert location.subregion == cities[0].subregion
    assert location.region == cities[0].region
    assert location.country == cities[0].country


def test_location_autofiller_set_from_district(
    cities: List[City],
    districts: List[District],
):
    """Should autofill location from a district."""
    location = AbstractLocation()
    location.district = districts[0]
    location.city = cities[1]
    LocationAutofiller(location).autofill_location()

    assert location.district == districts[0]
    assert location.city == districts[0].city
    assert location.subregion == districts[0].city.subregion
    assert location.region == districts[0].city.region
    assert location.country == districts[0].city.country


def test_location_autofiller_set_from_postal_code(
    districts: List[District],
    postal_codes: List[PostalCode],
):
    """Should autofill location from a postal code."""
    location = AbstractLocation()
    location.district = districts[0]
    location.postal_code = postal_codes[0]
    LocationAutofiller(location).autofill_location()

    assert location.postal_code == postal_codes[0]
    assert location.district == postal_codes[0].district
    assert location.city == postal_codes[0].city
    assert location.subregion == postal_codes[0].subregion
    assert location.region == postal_codes[0].region
    assert location.country == postal_codes[0].country


def test_location_autofiller_skip():
    """Should return a location object unmodified."""
    location = AbstractLocation()
    location.country = None
    location.region = None
    location.subregion = None
    location.city = None
    location.district = None
    location.postal_code = None

    LocationAutofiller(location).autofill_location()
    assert location.country is None
    assert location.region is None
    assert location.subregion is None
    assert location.city is None
    assert location.district is None
    assert location.postal_code is None
