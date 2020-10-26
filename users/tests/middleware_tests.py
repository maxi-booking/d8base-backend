"""The middleware tests module."""
from datetime import timedelta
from typing import Optional

import arrow
import pytest
from django.conf import settings
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from users.middleware import UserTimezoneMiddleware
from users.models import User

pytestmark = pytest.mark.django_db


def test_user_timezone_middleware(
    user: User,
    user_languages: QuerySet,
    client_with_token: Client,
):
    """Should set the timezone of the current user."""
    lang = user_languages.filter(user=user).first()

    def get_offset(header: Optional[str] = None) -> timedelta:
        """Return a date offset."""
        response = client_with_token.get(
            reverse(
                "user-languages-detail",
                args=[lang.pk],
            ),
            **{UserTimezoneMiddleware.TIME_ZONE_HEADER: header},
        )
        assert timezone.get_current_timezone_name() == settings.TIME_ZONE
        return arrow.get(response.json()["created"]).utcoffset()

    assert get_offset() == arrow.utcnow().utcoffset()

    user.locations.create(timezone="Europe/London")
    assert get_offset() == arrow.now("Europe/London").utcoffset()

    user.locations.all().delete()
    user.locations.create(timezone="America/Toronto")
    assert get_offset() == arrow.now("America/Toronto").utcoffset()

    user.locations.all().delete()
    assert get_offset() == arrow.utcnow().utcoffset()

    assert get_offset(
        header="Europe/Moscow") == arrow.now("Europe/Moscow").utcoffset()
    assert get_offset(
        header="Europe/London") == arrow.now("Europe/London").utcoffset()
    assert get_offset(header="invalid") == arrow.utcnow().utcoffset()
    assert get_offset() == arrow.utcnow().utcoffset()
