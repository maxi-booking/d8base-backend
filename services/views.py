"""The services views module."""
from django.conf import settings
from djmoney.contrib.exchange.models import Rate
from rest_framework import viewsets
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from d8b.viewsets import AllowAnyViewSetMixin

from .filtersets import (PriceFilterSet, ServiceFilterSet,
                         ServiceLocationFilterSet, ServicePhotoFilterSet,
                         ServiceTagFilterSet)
from .models import Price, Service, ServiceLocation, ServicePhoto, ServiceTag
from .serializers import (PriceSerializer, RateSerializer,
                          ServiceListSerializer, ServiceLocationSerializer,
                          ServicePhotoListSerializer, ServicePhotoSerializer,
                          ServiceSerializer, ServiceTagListSerializer,
                          ServiceTagSerializer)


class ServiceViewSet(viewsets.ModelViewSet):
    """The service viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "professional__user"
    serializer_class = ServiceSerializer
    queryset = Service.objects.get_list()
    search_fields = ("=id", "name", "description")
    filterset_class = ServiceFilterSet


class ServiceListViewSet(
        AllowAnyViewSetMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The service viewset."""

    serializer_class = ServiceListSerializer
    queryset = Service.objects.get_extended_list()
    search_fields = ("=id", "name", "description")
    filterset_fields = ("professional", "is_enabled")


class PriceViewSet(viewsets.ModelViewSet):
    """The price viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "service__professional__user"
    serializer_class = PriceSerializer
    queryset = Price.objects.get_list()
    search_fields = ("=id", "name")
    filterset_class = PriceFilterSet


class ServiceTagViewSet(viewsets.ModelViewSet):
    """The service tag viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "service__professional__user"
    serializer_class = ServiceTagSerializer
    queryset = ServiceTag.objects.get_list()
    search_fields = ("=id", "name")
    filterset_class = ServiceTagFilterSet


class ServiceLocationViewSet(viewsets.ModelViewSet):
    """The service location viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "service__professional__user"
    serializer_class = ServiceLocationSerializer
    queryset = ServiceLocation.objects.get_list()
    filterset_class = ServiceLocationFilterSet


class ServiceTagListViewSet(
        AllowAnyViewSetMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The service tag list viewset."""

    serializer_class = ServiceTagListSerializer
    queryset = ServiceTag.objects.get_names()
    search_fields = ("name", )


class ServicePhotoViewSet(viewsets.ModelViewSet):
    """The service photo viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = "service__professional__user"
    serializer_class = ServicePhotoSerializer
    queryset = ServicePhoto.objects.get_list()
    search_fields = ("=id", "name", "description")
    filterset_class = ServicePhotoFilterSet


class ServicePhotoListViewSet(
        AllowAnyViewSetMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The service photo list viewset."""

    serializer_class = ServicePhotoListSerializer
    queryset = ServicePhoto.objects.get_list()
    search_fields = ("=id", "name", "description")
    filterset_fields = ("service", "service__professional")


class RateViewSet(
        CacheResponseMixin,
        AllowAnyViewSetMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The rate viewset."""

    pagination_class = None
    queryset = Rate.objects.filter(
        currency__in=settings.CURRENCIES).order_by("currency")
    serializer_class = RateSerializer
    filterset_fields = ("currency", )
