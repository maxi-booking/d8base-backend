"""The location documents tests module."""
from typing import List

import pytest
from cities.models import AlternativeName, City

from location.documents import CityDocument

pytestmark = pytest.mark.django_db


def test_city_document_prepare_name(cities: List[City]):
    """Should return the name translations as a concatenated string."""
    city = cities[0]
    city.name = "test_en"
    city.name_de = "test_de"
    city.name_fr = "test_fr"
    city.name_ru = "test_ru"
    assert CityDocument().prepare_name(
        city) == "test_en test_en test_de test_fr test_ru"


def test_city_document_prepare_name_std(cities: List[City]):
    """Should return the name translations as a concatenated string."""
    city = cities[0]
    city.name_std = "test_en"
    city.name_std_de = "test_de"
    city.name_std_fr = "test_fr"
    city.name_std_ru = "test_ru"
    assert CityDocument().prepare_name_std(
        city) == "test_en test_en test_de test_fr test_ru"


def test_city_document_prepare_alt_names(cities: List[City]):
    """Should return the alt names as a concatenated string."""
    name_one = AlternativeName.objects.create(name="one")
    name_two = AlternativeName.objects.create(name="two")
    city = cities[0]
    city.alt_names.add(name_one, name_two)
    assert CityDocument().prepare_alt_names(city) == "one two"


def test_city_document_get_queryset(cities: List[City]):
    """Should return a queryset."""
    assert CityDocument().get_queryset().count() == len(cities)
