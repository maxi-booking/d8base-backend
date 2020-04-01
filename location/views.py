"""The location views module."""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from d8b.viewsets import AllowAnyViewSetMixin, DistanceFilterViewSetMixin

from .repositories import (AlternativeNameRepository, CityRepository,
                           ContinentRepository, CountryRepository,
                           DistrictRepository, LanguageRepository,
                           PostalCodeRepository, RegionRepository,
                           SubregionRepository)
from .serializers import (AlternativeNameSerializer, CitySerializer,
                          ContinentSerializer, CountrySerializer,
                          DistrictSerializer, LanguageSerializer,
                          PostalCodeSerializer, RegionSerializer,
                          SubregionSerializer)


class ContinentViewSet(
        CacheResponseMixin,
        AllowAnyViewSetMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The Continent viewset."""

    serializer_class = ContinentSerializer
    queryset = ContinentRepository().get_list()


class CountryViewSet(
        CacheResponseMixin,
        AllowAnyViewSetMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The Country viewset."""

    serializer_class = CountrySerializer
    queryset = CountryRepository().get_list()

    search_fields = ('=id', 'name', 'alt_names__name', 'slug', 'code', 'code3',
                     'tld', 'capital', 'language_codes')

    filterset_fields = ('currency', 'continent', 'code', 'code3', 'tld')


class RegionViewSet(
        CacheResponseMixin,
        AllowAnyViewSetMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The Region viewset."""

    serializer_class = RegionSerializer
    queryset = RegionRepository().get_list()

    search_fields = ('=id', 'name', 'name_std', 'alt_names__name', 'slug',
                     'code')

    filterset_fields = ('country', 'code')


class SubregionViewSet(
        CacheResponseMixin,
        AllowAnyViewSetMixin,
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
        AllowAnyViewSetMixin,
        DistanceFilterViewSetMixin,
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
        AllowAnyViewSetMixin,
        DistanceFilterViewSetMixin,
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
        AllowAnyViewSetMixin,
        DistanceFilterViewSetMixin,
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
        AllowAnyViewSetMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The AlternativeName viewset."""

    serializer_class = AlternativeNameSerializer
    queryset = AlternativeNameRepository().get_list()

    search_fields = ('=id', 'name', 'slug')

    filterset_fields = ('kind', 'language_code', 'is_preferred', 'is_short',
                        'is_colloquial', 'is_historic')


class ListLanguagesView(CacheResponseMixin, viewsets.ViewSet):
    """List all languages."""

    serializer = LanguageSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Return a list of all languages."""
        langs = LanguageRepository().get_list()
        serializer = self.serializer(langs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Return a language object."""
        try:
            lang = LanguageRepository().get(kwargs['pk'])
        except ObjectDoesNotExist:
            raise NotFound
        serializer = self.serializer(lang)
        return Response(serializer.data)
