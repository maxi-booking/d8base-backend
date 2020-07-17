"""The location filtersets module."""
from cities.models import City
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from location.repositories import CityRepository


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    """The number in filter class."""


class CityFilterSet(filters.FilterSet):
    """The filter class for the city viewset class."""

    repository: CityRepository = CityRepository()

    by_name = filters.CharFilter(
        label=_("By name"),
        method="filter_by_name",
    )

    def filter_by_name(self, queryset, _, value):
        """Filter a contact list based on the specified country."""
        # pylint: disable=no-self-use
        return self.repository.find_by_name(name=value, queryset=queryset)

    class Meta:
        """The city filter class serializer META class."""

        model = City
        fields = ("by_name", "country", "region", "subregion", "timezone")
