"""The location filtersets module."""
from cities.models import City, PostalCode
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from location.repositories import CityRepository, PostalCodeRepository


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    """The number in filter class."""


class PostalCodeFilterSet(filters.FilterSet):
    """The filter class for the postal code viewset class."""

    repository: PostalCodeRepository = PostalCodeRepository()

    city = filters.CharFilter(
        label=_("city"),
        method="filter_by_city",
    )

    def filter_by_city(self, queryset, _, value):
        """Filter postal codes by the city."""
        # pylint: disable=no-self-use
        return self.repository.find_by_city(
            city_id=int(value),
            queryset=queryset,
        )

    class Meta:
        """The metainformation."""

        model = PostalCode
        fields = ("country", "region", "subregion", "district")


class CityFilterSet(filters.FilterSet):
    """The filter class for the city viewset class."""

    repository: CityRepository = CityRepository()

    by_name = filters.CharFilter(
        label=_("By name"),
        method="filter_by_name",
    )

    def filter_by_name(self, queryset, _, value):
        """Filter cities by the name."""
        # pylint: disable=no-self-use
        return self.repository.find_by_name(name=value, queryset=queryset)

    class Meta:
        """The city filter class serializer META class."""

        model = City
        fields = ("by_name", "country", "region", "subregion", "timezone")
