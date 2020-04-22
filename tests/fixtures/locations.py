"""The location fixtures module."""

from typing import List

import pytest
from cities.models import (AlternativeName, City, Continent, Country, District,
                           Place, PostalCode, Region, Subregion)
from django.contrib.gis.geos import Point

from conftest import OBJECTS_TO_CREATE
from location.repositories import (AlternativeNameRepository, BaseRepository,
                                   CityRepository, ContinentRepository,
                                   CountryRepository, DistrictRepository,
                                   PostalCodeRepository, RegionRepository,
                                   SubregionRepository)


# pylint: disable=redefined-outer-name
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
        timezone='Europe/Paris',
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
