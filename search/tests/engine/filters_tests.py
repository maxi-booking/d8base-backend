"""The search engine filters tests module."""

from typing import List

import arrow
import pytest
from cities.models import (City, Country, District, PostalCode, Region,
                           Subregion)
from django.db.models.query import QuerySet
from moneyed import EUR, GBP, USD, Money

from search.engine import filters
from search.engine.request import SearchRequest
from services.models import Price, ServicePhoto
from users.models import User

pytestmark = pytest.mark.django_db
# pylint: disable=protected-access,redefined-outer-name,unused-argument


def test_dates_filter_professional(
    services: QuerySet,
    professional_schedules: QuerySet,
):
    """Should filter the query."""
    services.update(is_base_schedule=True)
    request = SearchRequest()
    handler = filters.DatesHandler()
    today = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    assert not handler._check_request(request)
    assert services.count() > 1

    request.start_datetime = today.shift(weekday=6)
    request.end_datetime = today.shift(weekday=6, hours=1)
    assert handler.handle(request, services).count() == 0

    request.start_datetime = today.shift(weekday=4)
    request.end_datetime = today.shift(weekday=4, hours=1)
    assert handler.handle(request, services).count() == 0

    request.start_datetime = today.shift(weekday=4, hours=10)
    request.end_datetime = today.shift(weekday=4, hours=14)
    assert handler.handle(request, services).count() > 1

    request.start_datetime = today.shift(weekday=4, hours=10)
    request.end_datetime = None
    assert handler.handle(request, services).count() > 1

    request.start_datetime = None
    request.end_datetime = today.shift(weekday=4, hours=14)
    assert handler.handle(request, services).count() > 1


def test_dates_filter_service(
    services: QuerySet,
    service_schedules: QuerySet,
):
    """Should filter the query."""
    services.update(is_base_schedule=False)
    request = SearchRequest()
    handler = filters.DatesHandler()
    today = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    assert not handler._check_request(request)
    assert services.count() > 1

    request.start_datetime = today.shift(weekday=6)
    request.end_datetime = today.shift(weekday=6, hours=1)
    assert handler.handle(request, services).count() == 0

    request.start_datetime = today.shift(weekday=4)
    request.end_datetime = today.shift(weekday=4, hours=1)
    assert handler.handle(request, services).count() == 0

    request.start_datetime = today.shift(weekday=4, hours=10)
    request.end_datetime = today.shift(weekday=4, hours=14)
    assert handler.handle(request, services).count() > 1

    request.start_datetime = today.shift(weekday=4, hours=10)
    request.end_datetime = None
    assert handler.handle(request, services).count() > 1

    request.start_datetime = None
    request.end_datetime = today.shift(weekday=4, hours=14)
    assert handler.handle(request, services).count() > 1


def test_price_filter(services: QuerySet):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.PriceHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.service.start_price = Money("1.3", GBP)
    assert handler.handle(request, services).count() == 0

    request.service.start_price = Money(5, EUR)
    request.service.end_price = Money(7, EUR)
    assert handler.handle(request, services).count() == 0

    request.service.start_price = Money(5, EUR)
    request.service.end_price = Money(10, EUR)
    assert handler.handle(request, services).count() > 1

    request.service.start_price = Money(5, USD)
    request.service.end_price = Money(99, USD)
    assert handler.handle(request, services).count() == 0


def test_only_with_photos_filter(services: QuerySet):
    """Should filter the query."""
    ServicePhoto.objects.all().delete()
    request = SearchRequest()
    handler = filters.OnlyWithPhotosHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.service.only_with_photos = True
    assert handler.handle(request, services).count() == 0

    services.filter(is_enabled=True).first().photos.create(name="test")
    assert handler.handle(request, services).count() == 1


def test_service_types_filter(services: QuerySet):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.ServiceTypesHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.service.service_types = ["invalid"]  # type: ignore
    assert handler.handle(request, services).count() == 0

    request.service.service_types = ["invalid", "online"]  # type: ignore
    assert handler.handle(request, services).count() > 1


def test_payment_methods_filter(services: QuerySet):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.PaymentMethodsHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.service.payment_methods = ["invalid"]  # type: ignore
    assert handler.handle(request, services).count() == 0

    request.service.payment_methods = ["invalid", "online"]  # type: ignore
    assert handler.handle(request, services).count() > 1


def test_only_with_fixed_price_filter(services: QuerySet):
    """Should filter the query."""
    Price.objects.update(is_price_fixed=False)
    request = SearchRequest()
    handler = filters.OnlyWithFixedPriceHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.service.only_with_fixed_price = True
    assert handler.handle(request, services).count() == 0

    Price.objects.update(is_price_fixed=True)

    assert handler.handle(request, services).count() > 1


def test_only_with_auto_order_confirmation_filter(services: QuerySet):
    """Should filter the query."""
    services.update(is_auto_order_confirmation=False)
    request = SearchRequest()
    handler = filters.OnlyWithAutoOrderConfirmationHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.service.only_with_auto_order_confirmation = True
    assert handler.handle(request, services).count() == 0

    services.update(is_auto_order_confirmation=True)
    assert handler.handle(request, services).count() > 1


def test_subcategories_filter(services: QuerySet, subcategories: QuerySet):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.SubcategoriesHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.service.subcategories = [subcategories.last()]
    assert handler.handle(request, services).count() == 0

    request.service.subcategories = [subcategories[1]]
    assert handler.handle(request, services).count() > 1


def test_categories_filter(services: QuerySet, categories: QuerySet):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.CategoriesHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.service.categories = [categories.last()]
    assert handler.handle(request, services).count() == 0

    request.service.categories = [categories.first()]
    assert handler.handle(request, services).count() > 1


def test_experience_filter(services: QuerySet):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.ExperienceHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.professional.experience = 4
    assert handler.handle(request, services).count() == 0

    request.professional.experience = 12
    assert handler.handle(request, services).count() > 1


def test_nationalites_filter(services: QuerySet, countries: List[Country]):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.NationalitiesHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.professional.nationalities = [countries[0], countries[1]]
    assert handler.handle(request, services).count() == 0

    user = services.first().professional.user
    user.nationality = countries[2]
    user.save()

    assert handler.handle(request, services).count() == 0

    request.professional.nationalities = [countries[2], countries[1]]
    assert handler.handle(request, services).count() > 1


def test_languages_filter(services: QuerySet, user_languages: QuerySet):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.LanguagesHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.professional.languages = ["aa", "bb"]
    assert handler.handle(request, services).count() == 0

    request.professional.languages = ["en", "ru", "aa"]
    assert handler.handle(request, services).count() > 1


def test_professional_filter(services: QuerySet):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.ProfessionalLevelHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.professional.professional_level = "invalid"  # type: ignore
    assert handler.handle(request, services).count() == 0

    request.professional.professional_level = "senior"
    assert handler.handle(request, services).count() == 2


def test_age_filter(services: QuerySet):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.AgeHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.professional.start_age = 10
    assert handler.handle(request, services).count() == 0

    user = services.first().professional.user
    user.birthday = arrow.utcnow().shift(years=-15).date()
    user.save()

    assert handler.handle(request, services).count() == 4

    request.professional.end_age = 12
    assert handler.handle(request, services).count() == 0

    request.professional.end_age = 17
    assert handler.handle(request, services).count() == 4

    request.professional.start_age = 15
    request.professional.end_age = 15
    assert handler.handle(request, services).count() == 4


def test_gender_filter(services: QuerySet):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.GenderHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.professional.gender = 1
    assert handler.handle(request, services).count() == 0

    request.professional.gender = 0
    assert handler.handle(request, services).count() == 0

    user = services.first().professional.user
    user.gender = 0
    user.save()

    assert handler.handle(request, services).count() == 4


def test_only_with_certificates_filter(services: QuerySet):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.OnlyWithCertificatesHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.professional.only_with_certificates = True
    assert handler.handle(request, services).count() == 0

    professional = services.first().professional
    professional.certificates.create(name="test certificate")

    assert handler.handle(request, services).count() == 2


def test_only_with_reviews_filter(services: QuerySet, user: User):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.OnlyWithReviewsHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.professional.only_with_reviews = True
    assert handler.handle(request, services).count() == 0

    professional = services.first().professional
    professional.reviews.create(user=user, title="test review", rating=2)

    assert handler.handle(request, services).count() == 2


def test_rating_filter(services: QuerySet):
    """Should filter the query."""
    professional = services.first().professional
    professional.rating = 4
    professional.save()
    request = SearchRequest()
    handler = filters.RatingHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.professional.rating = 3
    assert handler.handle(request, services).count() == 0

    request.professional.rating = 4
    assert handler.handle(request, services).count() == 2


def test_tag_filter(services: QuerySet):
    """Should filter the query."""
    request = SearchRequest()
    handler = filters.TagsHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.tags = ["invalid", "oops"]
    assert handler.handle(request, services).count() == 0

    request.tags = ["one", "invalid"]
    assert handler.handle(request, services).count() > 1


def test_country_filter(services: QuerySet, countries: List[Country]):
    """Should filter the query."""
    services.update(is_enabled=True)
    request = SearchRequest()
    handler = filters.CountryHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.location.country = countries[1]
    assert handler.handle(request, services).count() == 0

    request.location.country = countries[0]
    assert handler.handle(request, services).count() > 1


def test_region_filter(services: QuerySet, regions: List[Region]):
    """Should filter the query."""
    services.update(is_enabled=True)
    request = SearchRequest()
    handler = filters.RegionHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.location.region = regions[1]
    assert handler.handle(request, services).count() == 0

    request.location.region = regions[0]
    assert handler.handle(request, services).count() > 1


def test_subregion_filter(services: QuerySet, subregions: List[Subregion]):
    """Should filter the query."""
    services.update(is_enabled=True)
    request = SearchRequest()
    handler = filters.SubregionHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.location.subregion = subregions[1]
    assert handler.handle(request, services).count() == 0

    request.location.subregion = subregions[0]
    assert handler.handle(request, services).count() > 1


def test_city_filter(services: QuerySet, cities: List[City]):
    """Should filter the query."""
    services.update(is_enabled=True)
    request = SearchRequest()
    handler = filters.CityHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.location.city = cities[1]
    assert handler.handle(request, services).count() == 0

    request.location.city = cities[0]
    assert handler.handle(request, services).count() > 1


def test_district_filter(services: QuerySet, districts: List[District]):
    """Should filter the query."""
    services.update(is_enabled=True)
    request = SearchRequest()
    handler = filters.DistrictHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.location.district = districts[1]
    assert handler.handle(request, services).count() == 0

    request.location.district = districts[0]
    assert handler.handle(request, services).count() > 1


def test_postal_code_filter(
    services: QuerySet,
    postal_codes: List[PostalCode],
):
    """Should filter the query."""
    services.update(is_enabled=True)
    request = SearchRequest()
    handler = filters.PostalCodeHandler()
    assert not handler._check_request(request)
    assert services.count() > 1

    request.location.postal_code = postal_codes[2]
    assert handler.handle(request, services).count() == 0

    request.location.postal_code = postal_codes[1]
    assert handler.handle(request, services).count() > 1
