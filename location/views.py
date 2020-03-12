"""The location views module."""
from rest_framework import viewsets
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .repositories import (AlternativeNameRepository, CityRepository,
                           ContinentRepository, CountryRepository,
                           DistrictRepository, PostalCodeRepository,
                           RegionRepository, SubregionRepository)
from .serializers import (AlternativeNameSerializer, CitySerializer,
                          ContinentSerializer, CountrySerializer,
                          DistrictSerializer, PostalCodeSerializer,
                          RegionSerializer, SubregionSerializer)


class ContinentViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    """The Continent viewset."""

    serializer_class = ContinentSerializer
    queryset = ContinentRepository().get_list()


class CountryViewSet(
        CacheResponseMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The Country viewset."""

    serializer_class = CountrySerializer
    queryset = CountryRepository().get_list()

    search_fields = ('=id', 'name', 'alt_names__name', 'slug', 'code', 'code3',
                     'tld', 'capital', 'language_codes')

    filterset_fields = ('currency', 'continent')


class RegionViewSet(
        CacheResponseMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The Region viewset."""

    serializer_class = RegionSerializer
    queryset = RegionRepository().get_list()

    search_fields = ('=id', 'name', 'name_std', 'alt_names__name', 'slug',
                     'code')

    filterset_fields = ('country', )


class SubregionViewSet(
        CacheResponseMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The Subregion viewset."""

    serializer_class = SubregionSerializer
    queryset = SubregionRepository().get_list()

    search_fields = ('=id', 'name', 'name_std', 'alt_names__name', 'slug',
                     'code', 'region__name', 'region__name_std')

    filterset_fields = ('region', 'region__country')


class CityViewSet(
        CacheResponseMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The City viewset."""

    serializer_class = CitySerializer
    queryset = CityRepository().get_list()

    search_fields = ('=id', 'name', 'name_std', 'alt_names__name', 'slug',
                     'region__name', 'region__name_std', 'subregion__name',
                     'subregion__name_std')

    filterset_fields = ('country', 'region', 'subregion', 'timezone')


class DistrictViewSet(
        CacheResponseMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The District viewset."""

    serializer_class = DistrictSerializer
    queryset = DistrictRepository().get_list()

    search_fields = ('=id', 'name', 'name_std', 'alt_names__name', 'slug',
                     'city_name', 'city__name_std')

    filterset_fields = ('city', )


class PostalCodeViewSet(
        CacheResponseMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The PostalCode viewset."""

    serializer_class = PostalCodeSerializer
    queryset = PostalCodeRepository().get_list()

    search_fields = ('=id', 'name', 'alt_names__name', 'slug', 'region_name',
                     'subregion_name', 'district_name', 'country__name',
                     'region__name', 'subregion__name', 'city__name',
                     'district__name')

    filterset_fields = ('country', 'region', 'subregion', 'city', 'district')


class AlternativeNameViewSet(
        CacheResponseMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The AlternativeName viewset."""

    serializer_class = AlternativeNameSerializer
    queryset = AlternativeNameRepository().get_list()

    search_fields = ('=id', 'name', 'slug')

    filterset_fields = ('kind', 'language_code', 'is_preferred', 'is_short',
                        'is_colloquial', 'is_historic')
