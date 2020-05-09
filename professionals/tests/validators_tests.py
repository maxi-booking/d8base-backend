"""The location services test module."""

import pytest
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from professionals.validators import validate_user_location
from users.models import User

pytestmark = pytest.mark.django_db


def test_location_autofiller_set_from_region(
    admin: User,
    user: User,
    professional_locations: QuerySet,
    user_locations: QuerySet,
):
    """Should autofill location from a region."""
    user_locations[0].user = admin
    location = professional_locations[0]
    location.user = user
    location.user_location = user_locations[0]

    with pytest.raises(ValidationError):
        validate_user_location(location)
