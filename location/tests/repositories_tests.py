"""The users admin test module."""
from typing import List

import pytest
from cities.models import Place

from conftest import OBJECTS_TO_CREATE
from location.repositories import (AlternativeNameRepository, BaseRepository,
                                   CityRepository, ContinentRepository,
                                   CountryRepository, DistrictRepository,
                                   PostalCodeRepository, RegionRepository,
                                   SubregionRepository)

pytestmark = pytest.mark.django_db


# pylint: disable=no-member
@pytest.mark.parametrize('repo,expected_count,entries', [
    (
        ContinentRepository(),
        OBJECTS_TO_CREATE + 7,
        pytest.lazy_fixture('continents'),
    ),
    (
        CountryRepository(),
        OBJECTS_TO_CREATE,
        pytest.lazy_fixture('countries'),
    ),
    (
        RegionRepository(),
        OBJECTS_TO_CREATE,
        pytest.lazy_fixture('regions'),
    ),
    (
        SubregionRepository(),
        OBJECTS_TO_CREATE,
        pytest.lazy_fixture('subregions'),
    ),
    (
        CityRepository(),
        OBJECTS_TO_CREATE,
        pytest.lazy_fixture('cities'),
    ),
    (
        DistrictRepository(),
        OBJECTS_TO_CREATE,
        pytest.lazy_fixture('districts'),
    ),
    (
        PostalCodeRepository(),
        OBJECTS_TO_CREATE,
        pytest.lazy_fixture('postal_codes'),
    ),
    (
        AlternativeNameRepository(),
        OBJECTS_TO_CREATE,
        pytest.lazy_fixture('alternative_names'),
    ),
])
def test_repositories_get_list(
    repo: BaseRepository,
    expected_count: int,
    entries: List[Place],
):
    """Should return the a JSON response."""
    query = repo.get_list()
    assert query.count() == expected_count
    assert all(e in query for e in entries)
