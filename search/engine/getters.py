"""The search getters module."""
from abc import ABC, abstractmethod

from django.db.models import QuerySet

from d8b.settings import get_settings
from search.engine import filters
from services.documents import ServiceDocument
from services.models import Service

from .request import SearchRequest


class AbstractSearchGetter(ABC):
    """The abstract search getter class."""

    @abstractmethod
    def get_query(self, request: SearchRequest) -> QuerySet:
        """Return the getter result query."""


class ServiceSearchGetter(AbstractSearchGetter):
    """The service search getter class."""

    request: SearchRequest

    @staticmethod
    def _get_filters() -> filters.Handler:
        """Return the filters."""
        country = filters.CountryHandler()

        country.set_next(filters.RegionHandler()). \
            set_next(filters.SubregionHandler()). \
            set_next(filters.CityHandler()). \
            set_next(filters.DistrictHandler()). \
            set_next(filters.PostalCodeHandler()). \
            set_next(filters.DatesHandler()). \
            set_next(filters.TagsHandler()). \
            set_next(filters.RatingHandler()). \
            set_next(filters.OnlyWithReviewsHandler()). \
            set_next(filters.OnlyWithCertificatesHandler()). \
            set_next(filters.GenderHandler()). \
            set_next(filters.AgeHandler()). \
            set_next(filters.ProfessionalLevelHandler()). \
            set_next(filters.LanguagesHandler()). \
            set_next(filters.NationalitiesHandler()). \
            set_next(filters.ExperienceHandler()). \
            set_next(filters.CategoriesHandler()). \
            set_next(filters.SubcategoriesHandler()). \
            set_next(filters.OnlyWithAutoOrderConfirmationHandler()). \
            set_next(filters.OnlyWithFixedPriceHandler()). \
            set_next(filters.PaymentMethodsHandler()). \
            set_next(filters.ServiceTypesHandler()). \
            set_next(filters.OnlyWithPhotosHandler()). \
            set_next(filters.PriceHandler())

        return country

    def _get_base_query(self) -> QuerySet:
        """Return the getter result query."""
        query = Service.objects.filter(is_enabled=True)
        if self.request.query:
            result = ServiceDocument.search().query(
                "query_string",
                query=self.request.query,
            )[:get_settings("D8B_SEARCH_MAX_ENTRIES")]
            ids = {r.meta.id for r in result}
            query = query.filter(pk__in=ids)
        return query

    def get_query(self, request: SearchRequest) -> QuerySet:
        """Return the getter result query."""
        self.request = request
        query = self._get_base_query()
        query = self._get_filters().handle(request, query)
        return query
