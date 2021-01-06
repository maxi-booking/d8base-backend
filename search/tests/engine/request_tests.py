"""The search engine request tests module."""
from typing import List

import arrow
import pytest
from cities.models import Country, District, PostalCode
from django.conf import settings
from django.contrib.gis.geos.point import Point
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils import timezone
from djmoney.money import Money
from pytest_mock import MockFixture
from rest_framework.request import Request

from search.engine.request import (HTTPToSearchLocationRequestConverter,
                                   HTTPToSearchProfessionalRequestConverter,
                                   HTTPToSearchRequestConverter,
                                   HTTPToSearchServiceRequestConverter)

pytestmark = pytest.mark.django_db

# pylint: disable=protected-access


def test_http_search_service_request_converter_set_service_types():
    """Should set the service types."""
    request = HttpRequest()
    converter_class = HTTPToSearchServiceRequestConverter
    request.GET[converter_class.SERVICE_TYPES_PARAM] = "online, client, foo"

    converter = converter_class(Request(request))
    converter._set_service_types()

    assert sorted(converter.search_request.service.service_types) == [
        "client",
        "online",
    ]


def test_http_search_service_request_converter_set_payment_methods():
    """Should set the payment methods."""
    request = HttpRequest()
    converter_class = HTTPToSearchServiceRequestConverter
    request.GET[converter_class.PAYMENT_METHODS_PARAM] = "online, cash, foo"

    converter = converter_class(Request(request))
    converter._set_payment_methods()

    assert sorted(converter.search_request.service.payment_methods) == [
        "cash",
        "online",
    ]


def test_http_search_service_request_converter_set_price():
    """Should set the price."""
    request = HttpRequest()
    converter_class = HTTPToSearchServiceRequestConverter
    request.GET[converter_class.PRICE_CURRENCY_PARAM] = "EUR"
    request.GET[converter_class.START_PRICE_PARAM] = "12.5"

    converter = converter_class(Request(request))
    converter._set_price("start_price", converter_class.START_PRICE_PARAM)

    assert converter.search_request.service.start_price == Money("12.5", "EUR")

    request.GET[converter_class.PRICE_CURRENCY_PARAM] = "INVALID"
    request.GET[converter_class.END_PRICE_PARAM] = "33.5"
    converter = converter_class(Request(request))
    converter._set_price("end_price", converter_class.END_PRICE_PARAM)

    assert converter.search_request.service.end_price is None


def test_http_search_service_request_converter_get(subcategories: QuerySet):
    """Should set service params."""
    subcategory = subcategories.first()
    category = subcategory.category

    request = HttpRequest()
    converter_class = HTTPToSearchServiceRequestConverter
    request.GET[converter_class.CATEGORIES_PARAM] = f"{category.pk}"
    request.GET[converter_class.SUBCATEGORIES_PARAM] = f"{subcategory.pk}"
    request.GET[converter_class.ONLY_WITH_AUTO_ORDER_CONFIRMATION_PARAM] = "1"
    request.GET[converter_class.SERVICE_TYPES_PARAM] = "online, client, foo"
    request.GET[converter_class.ONLY_WITH_FIXED_PRICE_PARAM] = "1"
    request.GET[converter_class.PRICE_CURRENCY_PARAM] = "EUR"
    request.GET[converter_class.START_PRICE_PARAM] = "12.5"
    request.GET[converter_class.END_PRICE_PARAM] = "33.5"
    request.GET[converter_class.PAYMENT_METHODS_PARAM] = "online, cash, foo"
    request.GET[converter_class.ONLY_WITH_PHOTOS_PARAM] = "1"

    converter = converter_class(Request(request))
    result = converter.get().service

    assert result.categories == [category]
    assert result.subcategories == [subcategory]
    assert result.only_with_auto_order_confirmation
    assert sorted(converter.search_request.service.service_types) == [
        "client",
        "online",
    ]
    assert sorted(converter.search_request.service.payment_methods) == [
        "cash",
        "online",
    ]
    assert result.only_with_fixed_price
    assert converter.search_request.service.start_price == Money("12.5", "EUR")
    assert converter.search_request.service.end_price == Money("33.5", "EUR")
    assert result.only_with_photos


def test_http_search_professional_request_converter_get(
        countries: List[Country]):
    """Should set the professional params."""
    request = HttpRequest()
    converter_class = HTTPToSearchProfessionalRequestConverter
    request.GET[converter_class.GENDER_PARAM] = "1"
    request.GET[converter_class.PROFESSIONAL_LEVEL_PARAM] = "senior"
    request.GET[converter_class.LANGUAGES_PARAM] = "en,fr"
    request.GET[converter_class.RATING_PARAM] = "3"
    request.GET[converter_class.ONLY_WITH_REVIEWS_PARAM] = "1"
    request.GET[converter_class.ONLY_WITH_CERTIFICATES_PARAM] = "1"
    request.GET[converter_class.EXPERIENCE_PARAM] = "5"
    request.GET[converter_class.START_AGE_PARAM] = "25"
    request.GET[converter_class.END_AGE_PARAM] = "32"
    request.GET[converter_class.
                NATIONALITIES_PARAM] = f"{countries[0].pk}, {countries[1].pk}"

    converter = converter_class(Request(request))
    result = converter.get().professional

    assert result.gender == 1
    assert result.professional_level == "senior"
    assert sorted(result.languages) == ["en", "fr"]
    assert result.rating == 3
    assert result.only_with_reviews
    assert result.only_with_certificates
    assert result.experience == 5
    assert result.start_age == 25
    assert result.end_age == 32
    assert len(result.nationalities) == 2
    assert countries[0] in result.nationalities
    assert countries[1] in result.nationalities


def test_http_search_professional_request_converter_set_gender():
    """Should set the gender."""
    request = HttpRequest()
    request.GET[HTTPToSearchProfessionalRequestConverter.GENDER_PARAM] = "0"

    converter = HTTPToSearchProfessionalRequestConverter(Request(request))
    converter._set_gender()
    assert converter.search_request.professional.gender == 0

    request.GET[HTTPToSearchProfessionalRequestConverter.GENDER_PARAM] = "4"
    converter = HTTPToSearchProfessionalRequestConverter(Request(request))
    converter._set_gender()
    assert converter.search_request.professional.gender is None


def test_http_search_professional_request_converter_set_professional_level():
    """Should set the professional level."""
    request = HttpRequest()
    request.GET[HTTPToSearchProfessionalRequestConverter.
                PROFESSIONAL_LEVEL_PARAM] = "junior"

    converter = HTTPToSearchProfessionalRequestConverter(Request(request))
    converter._set_professional_level()

    assert converter.search_request.professional.professional_level == "junior"

    request.GET[HTTPToSearchProfessionalRequestConverter.
                PROFESSIONAL_LEVEL_PARAM] = "invalid"
    converter = HTTPToSearchProfessionalRequestConverter(Request(request))
    converter._set_professional_level()

    assert converter.search_request.professional.professional_level is None


def test_http_search_professional_request_converter_set_langauges():
    """Should set the languages."""
    request = HttpRequest()
    request.GET[
        HTTPToSearchProfessionalRequestConverter.LANGUAGES_PARAM] = "en,de"
    converter = HTTPToSearchProfessionalRequestConverter(Request(request))
    converter._set_languages()

    assert sorted(
        converter.search_request.professional.languages) == ["de", "en"]

    request.GET[
        HTTPToSearchProfessionalRequestConverter.LANGUAGES_PARAM] = "ru,xx"
    converter = HTTPToSearchProfessionalRequestConverter(Request(request))
    converter._set_languages()

    assert converter.search_request.professional.languages == ["ru"]

    request.GET[
        HTTPToSearchProfessionalRequestConverter.LANGUAGES_PARAM] = "xx,yy"
    converter = HTTPToSearchProfessionalRequestConverter(Request(request))
    converter._set_languages()

    assert converter.search_request.professional.languages == []


def test_http_search_location_request_converter_set_coordinate():
    """Should set the coordinate."""
    x = "-79.4163"
    y = "43.7001"
    request = HttpRequest()
    request.GET[HTTPToSearchLocationRequestConverter.COORDINATE_X_PARAM] = x
    request.GET[HTTPToSearchLocationRequestConverter.COORDINATE_Y_PARAM] = y
    converter = HTTPToSearchLocationRequestConverter(Request(request))
    converter._set_coordinate()

    assert converter.search_request.location.coordinate == Point(
        float(x),
        float(y),
    )

    request.GET[HTTPToSearchLocationRequestConverter.COORDINATE_Y_PARAM] = "!@"
    converter = HTTPToSearchLocationRequestConverter(Request(request))
    converter._set_coordinate()

    assert converter.search_request.location.coordinate is None


def test_http_search_location_request_set_invalid_country():
    """Must not set the country."""
    request = HttpRequest()
    converter_class = HTTPToSearchLocationRequestConverter
    request.GET[converter_class.COUNTRY_PARAM] = "999"

    converter = converter_class(Request(request))
    result = converter.get().location

    assert result.country is None


def test_http_search_location_request_converter_get(
    postal_codes: List[PostalCode],
    districts: List[District],
):
    """Should set the location params."""
    x = "-79.4163"
    y = "43.7001"
    postal_code: PostalCode = postal_codes[0]
    district = districts[0]
    city = postal_code.city
    subregion = postal_code.subregion
    region = postal_code.region
    country = postal_code.country
    request = HttpRequest()
    converter_class = HTTPToSearchLocationRequestConverter
    request.GET[converter_class.COORDINATE_X_PARAM] = x
    request.GET[converter_class.COORDINATE_Y_PARAM] = y
    request.GET[converter_class.COUNTRY_PARAM] = str(country.pk)
    request.GET[converter_class.REGION_PARAM] = str(region.pk)
    request.GET[converter_class.SUBREGION_PARAM] = str(subregion.pk)
    request.GET[converter_class.CITY_PARAM] = str(city.pk)
    request.GET[converter_class.DISTRICT_PARAM] = str(district.pk)
    request.GET[converter_class.POSTAL_CODE_PARAM] = str(postal_code.pk)
    request.GET[converter_class.MAX_DISTANCE_PARAM] = "12"

    converter = converter_class(Request(request))
    result = converter.get().location

    assert result.coordinate == Point(float(x), float(y))
    assert result.country == country
    assert result.region == region
    assert result.subregion == subregion
    assert result.city == city
    assert result.district == district
    assert result.postal_code == postal_code
    assert result.max_distance == 12

    request.GET[converter_class.COUNTRY_PARAM] = "0"
    converter = converter_class(Request(request))
    assert converter.get().location.country is None


def test_http_search_request_converter_set_query():
    """Should set the query string."""
    request = HttpRequest()
    request.GET[HTTPToSearchRequestConverter.QUERY_PARAM] = "test query"
    converter = HTTPToSearchRequestConverter(Request(request))
    converter._set_query()

    assert converter.search_request.query == "test query"


def test_http_search_request_converter_set_tags():
    """Should set the tags."""
    request = HttpRequest()
    request.GET[HTTPToSearchRequestConverter.TAGS_PARAM] = "one,two"
    converter = HTTPToSearchRequestConverter(Request(request))
    converter._set_tags()

    assert len(converter.search_request.tags) == 2
    assert "one" in converter.search_request.tags
    assert "two" in converter.search_request.tags


def test_http_search_request_converter_set_page():
    """Should set the page."""
    request = HttpRequest()
    request.GET[HTTPToSearchRequestConverter.PAGE_PARAM] = "3"
    converter = HTTPToSearchRequestConverter(Request(request))
    converter._set_page()

    assert converter.search_request.page == 3

    invalid_page = settings.D8B_SEARCH_MAX_PAGE + 1
    request.GET[HTTPToSearchRequestConverter.PAGE_PARAM] = str(invalid_page)
    converter = HTTPToSearchRequestConverter(Request(request))
    converter._set_page()

    assert converter.search_request.page == 1


def test_http_search_request_converter_set_datetime():
    """Should set the datetime."""
    timezone.deactivate()
    request = HttpRequest()
    param = HTTPToSearchRequestConverter.START_DATETIME_PARAM
    date_str = "2020-01-01T02:22:00"
    request.GET[param] = date_str
    converter = HTTPToSearchRequestConverter(Request(request))
    converter._set_datetime(param)

    assert converter.search_request.start_datetime == arrow.get(date_str)
    assert converter.search_request.start_datetime.tzinfo == arrow.utcnow(
    ).tzinfo

    request.GET[param] = date_str.split("T")[0]
    converter = HTTPToSearchRequestConverter(Request(request))
    converter._set_datetime(param)

    assert converter.search_request.start_datetime.datetime.hour == 0
    assert converter.search_request.start_datetime.datetime.minute == 0
    assert converter.search_request.start_datetime.datetime.second == 0

    timezone.activate("America/New_York")

    request.GET[param] = date_str
    converter = HTTPToSearchRequestConverter(Request(request))
    converter._set_datetime(param)

    expected = arrow.get(date_str, tzinfo="America/New_York")
    assert converter.search_request.start_datetime == expected.to("utc")
    assert converter.search_request.start_datetime.tzinfo == arrow.utcnow(
    ).tzinfo

    timezone.deactivate()

    request.GET[param] = "invalid"
    converter = HTTPToSearchRequestConverter(Request(request))
    converter._set_datetime(param)

    assert converter.search_request.start_datetime is None


def test_http_search_request_converter_get():
    """Should set the params."""
    timezone.deactivate()
    request = HttpRequest()
    start_str = "2199-01-01T02:22:00"
    end_str = "2199-01-02T02:22:00"
    request.GET[HTTPToSearchRequestConverter.START_DATETIME_PARAM] = start_str
    request.GET[HTTPToSearchRequestConverter.END_DATETIME_PARAM] = end_str
    request.GET[HTTPToSearchRequestConverter.QUERY_PARAM] = "test query"
    request.GET[HTTPToSearchRequestConverter.TAGS_PARAM] = "one,two"
    request.GET[HTTPToSearchRequestConverter.PAGE_PARAM] = "3"

    converter = HTTPToSearchRequestConverter(Request(request))
    result = converter.get()

    assert result.query == "test query"
    assert result.start_datetime == arrow.get(start_str)
    assert result.end_datetime == arrow.get(end_str)
    assert "one" in result.tags
    assert result.page == 3


def test_http_search_request_converter_get_converters(mocker: MockFixture):
    """Should run the converters."""
    professional_converter = mocker.patch(
        "search.engine.request.HTTPToSearchProfessionalRequestConverter.get")
    service_converter = mocker.patch(
        "search.engine.request.HTTPToSearchServiceRequestConverter.get")
    location_converter = mocker.patch(
        "search.engine.request.HTTPToSearchLocationRequestConverter.get")
    converter = HTTPToSearchRequestConverter(Request(HttpRequest()))
    converter.validator = mocker.Mock()
    converter.get()

    professional_converter.assert_called_once()
    service_converter.assert_called_once()
    location_converter.assert_called_once()

    converter.validator.assert_called_once_with(  # type: ignore
        converter.search_request)
