"""The commands test module."""
from typing import List

import pytest
from _pytest.capture import CaptureFixture
from cities.models import City, Continent, Country, District, Region, Subregion
from django.core.management import call_command
from pytest_mock import MockFixture

pytestmark = pytest.mark.django_db


def test_command_translate_cities(
    continents: List[Continent],
    countries: List[Country],
    regions: List[Region],
    subregions: List[Subregion],
    cities: List[City],
    districts: List[District],
    mocker: MockFixture,
):
    """Should translate the location objects."""
    translator = mocker.patch("location.repositories.translate")
    translator.return_value = "test"
    call_command("translate_cities", "de")
    total = sum([
        len(i) for i in (
            continents,
            countries,
            regions,
            subregions,
            cities,
            districts,
        )
    ]) + 7
    assert translator.call_count == total

    translator.call_count = 0
    call_command("translate_cities", "de")
    assert not translator.call_count


def test_command_translate_cities_exception(
    cities: List[City],
    mocker: MockFixture,
    capsys: CaptureFixture,
):
    """Should translate the location objects."""
    # pylint: disable=unused-argument
    mocker.patch(
        "location.repositories.translate",
        side_effect=Exception("test exception"),
    )
    call_command("translate_cities", "de")
    captured = capsys.readouterr()
    assert "test exception" in captured.err
