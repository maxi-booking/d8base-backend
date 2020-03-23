
"""The users models module."""
from typing import List

import pytest
from cities.models import City, Country

from users.models import User, UserLocation

pytestmark = pytest.mark.django_db


def test_user_location_save_autofill(
    user: User,
    countries: List[Country],
    cities: List[City],
):
    """Should call the LocationAutofiller on save."""
    user_location = UserLocation()
    user_location.user = user
    user_location.country = countries[0]
    user_location.city = cities[1]
    user_location.save()

    assert user_location.country == cities[1].country
    assert user_location.region == cities[1].region
    assert user_location.subregion == cities[1].subregion
    assert user_location.city == cities[1]
