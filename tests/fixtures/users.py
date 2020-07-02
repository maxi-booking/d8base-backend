"""The auth fixtures module."""
from typing import List

import pytest
from cities.models import Country, PostalCode
from django.contrib.gis.geos import Point
from django.db.models.query import QuerySet

from conftest import OBJECTS_TO_CREATE
from contacts.models import Contact
from users.models import (User, UserContact, UserLanguage, UserLocation,
                          UserSavedProfessional, UserSettings)


# pylint: disable=redefined-outer-name
@pytest.fixture
def contacts(countries: List[Country]) -> QuerySet:
    """Return a contacts queryset."""
    telegram, _ = Contact.objects.get_or_create(
        name='telegram',
        code='telegram_code',
    )
    icq, _ = Contact.objects.get_or_create(
        name='icq',
        code='icq_code',
    )
    whatsapp, _ = Contact.objects.get_or_create(
        name='whatsapp',
        code='whatsapp_code',
    )
    telegram.countries.add(countries[0])
    icq.excluded_countries.add(countries[1])
    whatsapp.excluded_countries.add(countries[0])

    return Contact.objects.get_list()


@pytest.fixture
def users() -> QuerySet:
    """Return a users queryset."""
    for i in range(0, OBJECTS_TO_CREATE):
        User.objects.create_user(
            email=f'user_{i}@example.com',
            password='pass',
            first_name='user_first_name_{i}',
            last_name='user_last_name_{i}',
        )
    return User.objects.filter(email__startswith='user_')


@pytest.fixture
def user_languages(admin: User, user: User) -> QuerySet:
    """Return a user languages queryset."""
    for i in (
        ('en', admin, True),
        ('fr', user, True),
        ('de', admin, False),
        ('ru', admin, False),
    ):
        UserLanguage.objects.create(language=i[0], user=i[1], is_native=i[2])
    return UserLanguage.objects.get_list()


@pytest.fixture
def user_settings(admin: User, user: User) -> QuerySet:
    """Return a user settings queryset."""
    for i in (
        ('en', 'UDS', admin),
        ('fr', 'EUR', user),
    ):
        UserSettings.objects.create(language=i[0], currency=i[1], user=i[2])
    return UserSettings.objects.get_list()


@pytest.fixture
def user_locations(
    admin: User,
    user: User,
    postal_codes: List[PostalCode],
) -> QuerySet:
    """Return a user locations queryset."""
    for k, i in enumerate((
        (admin, postal_codes[0], Point((13, 53))),
        (user, postal_codes[2], Point((13, 36))),
        (admin, postal_codes[1], Point((18, 11))),
        (user, postal_codes[3], Point((73, 93))),
    )):
        UserLocation.objects.create(
            user=i[0],
            postal_code=i[1],
            address=f'test address {k}',
            coordinates=i[2],
        )
    return UserLocation.objects.get_list()


@pytest.fixture
def user_contacts(
    admin: User,
    user: User,
    contacts: QuerySet,
) -> QuerySet:
    """Return a user contacts queryset."""
    for k, i in enumerate((
        (admin, contacts[0]),
        (user, contacts[1]),
        (admin, contacts[1]),
        (user, contacts[2]),
    )):
        UserContact.objects.create(
            user=i[0],
            contact=i[1],
            value=f'test contact {k}',
        )
    return UserContact.objects.get_list()


@pytest.fixture
def user_saved_professionals(
    admin: User,
    user: User,
    professionals: QuerySet,
) -> QuerySet:
    """Return a user saved professionals queryset."""
    for k, i in enumerate((
        (admin, professionals[0]),
        (user, professionals[1]),
        (admin, professionals[1]),
        (user, professionals[2]),
    )):
        UserSavedProfessional.objects.create(
            user=i[0],
            professional=i[1],
            note=f'professional note {k}',
        )
    return UserSavedProfessional.objects.get_list()
