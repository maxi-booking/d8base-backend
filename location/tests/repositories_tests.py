"""The users admin test module."""
from typing import List

import pytest
from cities.models import Place
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from conftest import OBJECTS_TO_CREATE
from location.repositories import (AlternativeNameRepository, BaseRepository,
                                   CityRepository, ContinentRepository,
                                   CountryRepository, DistrictRepository,
                                   LanguageRepository, PostalCodeRepository,
                                   RegionRepository, SubregionRepository)

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


def test_language_repository_get_list():
    """Should return a list of Languages."""
    langs = LanguageRepository().get_list()

    assert len(settings.LANGUAGES) == len(langs)
    assert langs[0].code == 'af'
    assert langs[0].name == 'Afrikaans'


def test_language_repository_get():
    """Should return a Language object."""
    lang = LanguageRepository().get('en')

    assert lang.code == 'en'
    assert lang.name == 'English'

    with pytest.raises(ObjectDoesNotExist):
        LanguageRepository().get('invalid')
