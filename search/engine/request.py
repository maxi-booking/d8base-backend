"""The search request module."""
from abc import ABC, abstractmethod
from decimal import InvalidOperation
from typing import Callable, List, Literal, Optional, Type

import arrow
from cities.models import (City, Country, District, PostalCode, Region,
                           Subregion)
from django.apps import apps
from django.conf import settings
from django.contrib.gis.geos.point import Point
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.timezone import get_current_timezone
from djmoney.money import Money
from moneyed import CurrencyDoesNotExist
from rest_framework.request import Request

from professionals.models import Category, Professional, Subcategory
from services.models import Price, Service
from users.models import User

from .validators import validate_search_request


class SearchLocationRequest():
    """The search location request class."""

    country: Optional[Country] = None
    region: Optional[Region] = None
    subregion: Optional[Subregion] = None
    city: Optional[City] = None
    district: Optional[District] = None
    postal_code: Optional[PostalCode] = None
    coordinate: Optional[Point] = None
    max_distance: Optional[int] = None


class SearchProfessionalRequest():
    """The search location request class."""

    rating: Optional[int] = None
    only_with_reviews: bool = False
    only_with_certificates: bool = False
    experience: Optional[int] = None
    gender: Optional[Literal[0, 1]] = None
    start_age: Optional[int] = None
    end_age: Optional[int] = None
    professional_level: Optional[Literal["junior", "middle", "senior"]] = None
    languages: List[str]
    nationalities: List[Country]

    def __init__(self):
        """Construct the object."""
        self.languages = []
        self.nationalities = []


class SearchServiceRequest():
    """The search location request class."""

    categories: List[Category]
    subcategories: List[Subcategory]
    only_with_auto_order_confirmation: bool = False
    service_types: List[Literal["online", "professional", "client"]]
    only_with_fixed_price: bool = False
    start_price: Optional[Money] = None
    end_price: Optional[Money] = None
    payment_methods: List[Literal["cash", "online"]]
    only_with_photos: bool = False

    def __init__(self):
        """Construct the object."""
        self.categories = []
        self.subcategories = []
        self.service_types = []
        self.payment_methods = []


class SearchRequest():
    """The search request class."""

    query: Optional[str] = None
    start_datetime: Optional[arrow.Arrow]
    end_datetime: Optional[arrow.Arrow]
    tags: List[str]

    professional: SearchProfessionalRequest
    service: SearchServiceRequest
    location: SearchLocationRequest

    def __init__(self):
        """Construct the object."""
        self.professional = SearchProfessionalRequest()
        self.service = SearchServiceRequest()
        self.location = SearchLocationRequest()
        self.tags = []


class AbstractHTTPConverter(ABC):
    """The abstract HTTP converter."""

    request: Request
    search_request: SearchRequest

    def __init__(
        self,
        request: Request,
        search_request: Optional[SearchRequest] = None,
    ):
        """Construct the object."""
        if not search_request:
            search_request = SearchRequest()
        self.search_request = search_request
        self.request = request
        self.validator: Callable[["SearchRequest"],
                                 None] = validate_search_request

    def _get_query_param(self, name: str) -> Optional[str]:
        """Get a param form the query params."""
        return self.request.query_params.get(name, None)

    def _get_list_param(self, name: str) -> List[str]:
        """Get a list param form the query params."""
        value = self._get_query_param(name)
        if value:
            return value.split(",")
        return []

    def _get_int_param(self, name: str) -> Optional[int]:
        """Get an int param form the query params."""
        value = self._get_query_param(name)
        if value and value.isnumeric():
            return int(value)
        return None

    def _get_bool_param(self, name: str) -> bool:
        """Get a bool param form the query params."""
        return bool(self._get_query_param(name))

    def _get_model_object(
        self,
        *,
        app: str,
        model: str,
        param: str,
    ) -> Optional[models.Model]:
        """Set an object to the request."""
        pk = self._get_int_param(param)
        if not pk:
            return None
        try:
            manager = apps.get_model(app, model).objects
            return manager.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    def _get_multiple_model_objects(
        self,
        *,
        app: str,
        model: str,
        param: str,
    ) -> List[models.Model]:
        """Set objects to the request."""
        pks = self._get_list_param(param)
        if not pks:
            return []
        pks = [p for p in pks if p.isnumeric()]
        manager = apps.get_model(app, model).objects
        result = list(manager.filter(pk__in=pks))
        return result

    @abstractmethod
    def get(self) -> SearchRequest:
        """Return the request."""


class HTTPToSearchLocationRequestConverter(AbstractHTTPConverter):
    """The http to search location request converter class."""

    COUNTRY_PARAM: str = "country"
    REGION_PARAM: str = "region"
    SUBREGION_PARAM: str = "subregion"
    CITY_PARAM: str = "city"
    DISTRICT_PARAM: str = "district"
    POSTAL_CODE_PARAM: str = "postal_code"
    COORDINATE_X_PARAM: str = "longitude"
    COORDINATE_Y_PARAM: str = "latitude"
    MAX_DISTANCE_PARAM: str = "max_distance"

    def _set_coordinate(self):
        """Set a coordinate to the search request."""
        x = self._get_query_param(self.COORDINATE_X_PARAM)
        y = self._get_query_param(self.COORDINATE_Y_PARAM)
        if x and y:
            self.search_request.location.coordinate = Point(x, y)

    def _set_max_distance(self):
        """Set a max distance to the search request."""
        distance = self._get_query_param(self.MAX_DISTANCE_PARAM)
        if distance.isnumeric():
            self.search_request.location.max_distance = int(distance)

    def get(self) -> SearchRequest:
        """Return the request."""
        self.search_request.location.country = self._get_model_object(
            app="cities",
            model="Country",
            param=self.COUNTRY_PARAM,
        )
        self.search_request.location.region = self._get_model_object(
            app="cities",
            model="Region",
            param=self.REGION_PARAM,
        )
        self.search_request.location.subregion = self._get_model_object(
            app="cities",
            model="Subregion",
            param=self.SUBREGION_PARAM,
        )
        self.search_request.location.city = self._get_model_object(
            app="cities",
            model="City",
            param=self.CITY_PARAM,
        )
        self.search_request.location.district = self._get_model_object(
            app="cities",
            model="District",
            param=self.DISTRICT_PARAM,
        )
        self.search_request.location.postal_code = self._get_model_object(
            app="cities",
            model="PostalCode",
            param=self.POSTAL_CODE_PARAM,
        )
        self.search_request.location.max_distance = self._get_int_param(
            self.MAX_DISTANCE_PARAM)
        self._set_coordinate()

        return self.search_request


class HTTPToSearchProfessionalRequestConverter(AbstractHTTPConverter):
    """The http to search professional request converter class."""

    RATING_PARAM: str = "rating"
    ONLY_WITH_REVIEWS_PARAM: str = "only_with_reviews"
    ONLY_WITH_CERTIFICATES_PARAM: str = "only_with_certificates"
    EXPERIENCE_PARAM: str = "experience"
    GENDER_PARAM: str = "gender"
    START_AGE_PARAM: str = "start_age"
    END_AGE_PARAM: str = "end_age"
    PROFESSIONAL_LEVEL_PARAM: str = "professional_level"
    LANGUAGES_PARAM: str = "languages"
    NATIONALITIES_PARAM: str = "nationalities"

    def _set_gender(self):
        """Set a gender to the search request."""
        gender = self._get_int_param(self.GENDER_PARAM)
        if gender in (User.GENDER_MALE, User.GENDER_FEMALE):
            self.search_request.professional.gender = gender

    def _set_professional_level(self):
        """Set a professional level to the search request."""
        level = self._get_query_param(self.GENDER_PARAM)
        if level in (
                Professional.LEVEL_JUNIOR,
                Professional.LEVEL_MIDDLE,
                Professional.LEVEL_SENIOR,
        ):
            self.search_request.professional.professional_level = level

    def _set_languages(self):
        """Set languages to the search request."""
        langs = self._get_list_param(self.LANGUAGES_PARAM)
        if not langs:
            return
        langs = list(set(langs) & set(settings.LANGUAGES_LIST))
        self.search_request.professional.languages = langs

    def get(self) -> SearchRequest:
        """Return the request."""
        self.search_request.professional.rating = self._get_int_param(
            self.RATING_PARAM)

        self.search_request.professional.only_with_reviews = \
            self._get_bool_param(self.ONLY_WITH_REVIEWS_PARAM)

        self.search_request.professional.only_with_certificates = \
            self._get_bool_param(self.ONLY_WITH_CERTIFICATES_PARAM)

        self.search_request.professional.experience = self._get_int_param(
            self.EXPERIENCE_PARAM)

        self._set_gender()

        self.search_request.professional.start_age = self._get_int_param(
            self.START_AGE_PARAM)

        self.search_request.professional.end_age = self._get_int_param(
            self.END_AGE_PARAM)

        self._set_professional_level()
        self._set_languages()

        self.search_request.professional.nationalities = \
            self._get_multiple_model_objects(
                app="cities",
                model="Country",
                param=self.NATIONALITIES_PARAM,
            )

        return self.search_request


class HTTPToSearchServiceRequestConverter(AbstractHTTPConverter):
    """The http to search service request converter class."""

    CATEGORIES_PARAM: str = "categories"
    SUBCATEGORIES_PARAM: str = "subcategories"
    ONLY_WITH_AUTO_ORDER_CONFIRMATION_PARAM: str = \
        "only_with_auto_order_confirmation"
    SERVICE_TYPES_PARAM: str = "service_types"
    ONLY_WITH_FIXED_PRICE_PARAM: str = "only_with_fixed_price"
    START_PRICE_PARAM: str = "start_price"
    END_PRICE_PARAM: str = "end_price"
    PRICE_CURRENCY_PARAM: str = "price_currency"
    PAYMENT_METHODS_PARAM: str = "payment_methods"
    ONLY_WITH_PHOTOS_PARAM: str = "only_with_photos"

    def _set_service_type(self):
        """Set service types to the search request."""
        types = self._get_list_param(self.SERVICE_TYPES_PARAM)
        allowed = [t[0] for t in Service.TYPE_CHOICES]
        return list(set(types) & set(allowed))

    def _set_payment_methods(self):
        """Set payment_methods to the search request."""
        types = self._get_list_param(self.PAYMENT_METHODS_PARAM)
        allowed = [m[0] for m in Price.PAYMENT_METHODS_CHOICES]
        return list(set(types) & set(allowed))

    def _set_price(self, attr: str, param: str):
        """Set a price to the search request."""
        currency = self._get_query_param(self.PRICE_CURRENCY_PARAM)
        if not currency:
            return
        price_value = self._get_query_param(param)
        try:
            price = Money(price_value, currency)
            setattr(self.search_request.service, attr, price)
        except (InvalidOperation, CurrencyDoesNotExist):
            pass

    def get(self) -> SearchRequest:
        """Return the request."""
        self.search_request.service.categories = \
            self._get_multiple_model_objects(
                app="professionals",
                model="Category",
                param=self.CATEGORIES_PARAM,
            )
        self.search_request.service.subcategories = \
            self._get_multiple_model_objects(
                app="professionals",
                model="Subcategory",
                param=self.SUBCATEGORIES_PARAM,
            )
        self.search_request.service.only_with_auto_order_confirmation = \
            self._get_bool_param(self.ONLY_WITH_AUTO_ORDER_CONFIRMATION_PARAM)

        self._set_service_type()

        self.search_request.service.only_with_fixed_price = \
            self._get_bool_param(self.ONLY_WITH_FIXED_PRICE_PARAM)

        self._set_price("start_price", self.START_PRICE_PARAM)
        self._set_price("end_price", self.END_PRICE_PARAM)

        self._set_payment_methods()
        self.search_request.service.only_with_photos = \
            self._get_bool_param(self.ONLY_WITH_PHOTOS_PARAM)

        return self.search_request


class HTTPToSearchRequestConverter(AbstractHTTPConverter):
    """The http to search request converter class."""

    QUERY_PARAM: str = "query"
    START_DATETIME_PARAM: str = "start_datetime"
    END_DATETIME_PARAM: str = "end_datetime"
    TAGS_PARAM: str = "tags"

    converters: List[Type] = [
        HTTPToSearchProfessionalRequestConverter,
        HTTPToSearchServiceRequestConverter,
        HTTPToSearchLocationRequestConverter,
    ]

    def _set_query(self):
        """Set a query to the request."""
        self.search_request.query = self._get_query_param(self.QUERY_PARAM)

    def _set_tags(self):
        """Set tags to the request."""
        self.search_request.tags = self._get_list_param(self.TAGS_PARAM)

    def _set_datetime(self, name: str):
        """Set a datetime to the calendart request."""
        date_str = str(self._get_query_param(name))
        try:
            date = arrow.get(date_str, tzinfo=get_current_timezone())
            setattr(self.search_request, name, date.to("utc"))
        except arrow.ParserError:
            pass

    def get(self) -> SearchRequest:
        """Convert and return the HTTP request to a search request."""
        self.search_request = SearchRequest()

        self._set_query()
        self._set_datetime(self.START_DATETIME_PARAM)
        self._set_datetime(self.END_DATETIME_PARAM)

        for converter_class in self.converters:
            converter = converter_class(
                request=self.request,
                search_request=self.search_request,
            )
            self.search_request = converter.get()

        self.validator(self.search_request)
        return self.search_request
