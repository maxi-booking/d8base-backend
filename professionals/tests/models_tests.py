
"""The users models module."""
from typing import List

import pytest
from cities.models import City, Country
from django.db.models import QuerySet

from professionals.models import ProfessionalLocation

pytestmark = pytest.mark.django_db


def test_professional_location_save_autofill(
    countries: List[Country],
    cities: List[City],
    professionals: QuerySet
):
    """Should call the LocationAutofiller on save."""
    professional_location = ProfessionalLocation()
    professional_location.professional = professionals[0]
    professional_location.country = countries[0]
    professional_location.city = cities[1]
    professional_location.save()

    assert professional_location.country == cities[1].country
    assert professional_location.region == cities[1].region
    assert professional_location.subregion == cities[1].subregion
    assert professional_location.city == cities[1]


def test_professional_location_save_copy_autofill(
    professionals: QuerySet,
    user_locations: QuerySet
):
    """Should call the LocationCopyAutofiller on save."""
    professional_location = ProfessionalLocation()
    professional_location.professional = professionals[0]
    professional_location.user_location = user_locations[0]
    professional_location.save()

    assert professional_location.country == user_locations[0].country
    assert professional_location.address == user_locations[0].address
