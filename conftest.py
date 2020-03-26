"""The pytest fixtures module."""
from typing import List

import pytest
from cities.models import (AlternativeName, City, Continent, Country, District,
                           Place, PostalCode, Region, Subregion)
from django.contrib.gis.geos import Point
from django.db.models.query import QuerySet
from django.test.client import Client
from rest_framework.test import APIClient

from d8b import middleware
from location.repositories import (AlternativeNameRepository, BaseRepository,
                                   CityRepository, ContinentRepository,
                                   CountryRepository, DistrictRepository,
                                   PostalCodeRepository, RegionRepository,
                                   SubregionRepository)
from users.models import User, UserLanguage, UserLocation
from users.registration import get_auth_tokens

collect_ignore_glob = ['*/migrations/*']  # pylint: disable=invalid-name

ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'admin_password'
USER_EMAIL = 'user@example.com'
USER_PASSWORD = 'user_password'
OBJECTS_TO_CREATE = 5


# pylint: disable=redefined-outer-name
@pytest.fixture()
def admin_client(admin: User) -> Client:
    """Return a Django test client logged in as an admin user."""
    client = Client()
    client.login(username=admin.email, password=ADMIN_PASSWORD)

    return client


@pytest.fixture()
def client_with_token(user: User) -> APIClient:
    """Return a Django test client logged with a token."""
    client = APIClient()
    access, _ = get_auth_tokens(user)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access.token)

    return client


def _create_location_objects(
        *,
        repo: BaseRepository,
        name: str,
        **kwargs,
) -> List[Place]:
    """Create a list of location objects."""
    result = []
    for i in range(0, OBJECTS_TO_CREATE):
        parsed_kwargs = {
            k: v.format(i) if isinstance(v, str) else v
            for (k, v) in kwargs.items()
        }
        result.append(repo.get_or_create(name=f'{name}_{i}', **parsed_kwargs))

    return result


@pytest.fixture
def continents() -> List[Continent]:
    """Return a list of continents."""
    return _create_location_objects(
        repo=ContinentRepository(),
        name='continent',
        code='C{}',
    )


@pytest.fixture
def countries() -> List[Country]:
    """Return a list of countries."""
    return _create_location_objects(
        repo=CountryRepository(),
        name='country',
        code='C{}',
        code3='CR{}',
        population=1234,
    )


@pytest.fixture
def regions(countries) -> List[Region]:
    """Return a list of regions."""
    return _create_location_objects(
        repo=RegionRepository(),
        name='region',
        code='R{}',
        country=countries[0],
    )


@pytest.fixture
def subregions(regions) -> List[Subregion]:
    """Return a list of subregions."""
    return _create_location_objects(
        repo=SubregionRepository(),
        name='subregion',
        code='S{}',
        region=regions[0],
    )


@pytest.fixture
def cities(countries, regions, subregions) -> List[City]:
    """Return a list of cities."""
    return _create_location_objects(
        repo=CityRepository(),
        name='city',
        population=2323,
        location=Point((10, 12)),
        country=countries[0],
        region=regions[0],
        subregion=subregions[0],
    )


@pytest.fixture
def districts(cities) -> List[District]:
    """Return a list of districts."""
    return _create_location_objects(
        repo=DistrictRepository(),
        name='district',
        code='D{}',
        population=2125,
        location=Point((22, 33)),
        city=cities[0],
    )


@pytest.fixture
def postal_codes(cities) -> List[PostalCode]:
    """Return a list of postal codes."""
    return _create_location_objects(
        repo=PostalCodeRepository(),
        name='postal_code',
        code='P{}',
        location=Point((23, 33)),
        country=cities[0].country,
        region=cities[0].region,
        subregion=cities[0].subregion,
        city=cities[0],
    )


@pytest.fixture
def alternative_names() -> List[AlternativeName]:
    """Return a list of alternative names."""
    return _create_location_objects(
        repo=AlternativeNameRepository(),
        name='alternative_name',
    )


@pytest.fixture
def admin() -> User:
    """Return an admin user."""
    return User.objects.create_superuser(
        ADMIN_EMAIL,
        ADMIN_PASSWORD,
    )


@pytest.fixture
def user() -> User:
    """Return a common user."""
    return User.objects.create_user(
        USER_EMAIL,
        USER_PASSWORD,
    )


@pytest.fixture(autouse=True)
def before_all():
    """Run before all tests."""
    # pylint: disable=protected-access
    middleware._USER.value = None


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
