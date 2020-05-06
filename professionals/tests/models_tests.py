
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
    user_location = ProfessionalLocation()
    user_location.professional = professionals[0]
    user_location.country = countries[0]
    user_location.city = cities[1]
    user_location.save()

    assert user_location.country == cities[1].country
    assert user_location.region == cities[1].region
    assert user_location.subregion == cities[1].subregion
    assert user_location.city == cities[1]
