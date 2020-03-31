
"""The users models module."""
from typing import List

import pytest
from cities.models import City, Country
from django.db.models.query import QuerySet

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


def test_user_location_save_set_default_field(
    user: User,
    user_locations: QuerySet,
    countries: List[Country],
):
    """Should call the DefaultFieldSetter on save."""
    query = user_locations.filter(user=user, is_default=True)
    old_default = query.first()

    new_default = UserLocation()
    new_default.user = user
    new_default.country = countries[0]
    new_default.is_default = True
    new_default.save()

    assert old_default.is_default
    old_default.refresh_from_db()
    assert not old_default.is_default
    assert new_default.is_default
    assert query.count() == 1