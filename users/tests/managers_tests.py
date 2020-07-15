"""The managers tests module."""
from typing import List

import pytest
from cities.models import Country
from django.conf import settings

from users.models import User, UserLanguage, UserLocation

pytestmark = pytest.mark.django_db

# pylint: disable=no-value-for-parameter


def test_user_location_manager_get_user_location(user: User):
    """Should a user timezone."""
    manager = UserLocation.objects
    assert manager.get_user_timezone(user) is None
    user.locations.create(timezone='Europe/London')
    assert manager.get_user_timezone(user) == 'Europe/London'


def test_user_manager_create_user():
    """Should create a user."""
    user = User.objects.create_user(email='common@user.com', password='foo')
    groups = user.groups.all()

    assert user.email == 'common@user.com'
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    assert user.username is None
    assert groups.count() == 1
    assert groups[0].name == settings.GROUP_USER_NAME
    with pytest.raises(TypeError):
        User.objects.create_user()  # type: ignore
    with pytest.raises(TypeError):
        User.objects.create_user(email='')  # type: ignore
    with pytest.raises(TypeError):
        User.objects.create_user(email='')  # type: ignore
    with pytest.raises(ValueError):
        User.objects.create_user(email='', password='foo')


def test_user_manager_create_superuser():
    """Should create a superuser."""
    user = User.objects.create_superuser('super@user.com', 'foo')

    assert user.email == 'super@user.com'
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser
    assert user.username is None

    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email='super@user.com',
            password='foo',
            is_superuser=False,
        )

    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email='super@user.com',
            password='foo',
            is_staff=False,
        )


def test_user_settings_manager_update_or_create_from_user_language(user: User):
    """Should update or create a user settings from the user language."""
    UserLanguage.objects.create(user=user, language='de')
    user.refresh_from_db()

    assert user.settings.language == 'de'

    user.settings.delete()
    UserLanguage.objects.create(user=user, language='xx')
    user.refresh_from_db()

    assert user.settings.language == 'en'


def test_user_settings_manager_update_or_create_from_user_location(
    user: User,
    countries: List[Country],
):
    """Should update or create a user settings from the user location."""
    countries[0].language_codes = 'fr'
    countries[0].currency = 'EUR'

    countries[1].language_codes = 'invalid'
    countries[1].currency = 'INVALID'

    UserLocation.objects.create(user=user, country=countries[0])
    user.refresh_from_db()

    assert user.settings.language == 'fr'
    assert user.settings.currency == 'EUR'
    assert user.settings.units == settings.UNITS_METRIC

    # invalid language and currency
    user.settings.delete()
    UserLocation.objects.create(
        user=user,
        country=countries[1],
        units=settings.UNITS_IMPERIAL,
    )
    user.refresh_from_db()

    assert user.settings.language == 'en'
    assert user.settings.currency == 'USD'
    assert user.settings.units == settings.UNITS_IMPERIAL

    # user location without a country
    user.settings.delete()
    UserLocation.objects.create(user=user)
    user.refresh_from_db()

    assert user.settings.language == 'en'
    assert user.settings.currency == 'USD'
    assert user.settings.units == settings.UNITS_METRIC
