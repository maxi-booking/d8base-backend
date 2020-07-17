"""The d8b viewsets module."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework_gis.filters import DistanceToPointFilter

from users.filters import OwnerFilter


class AllowAnyViewSetMixin():
    """The AllowAnyViewSetMixin."""

    permission_classes = [AllowAny]


class DistanceFilterViewSetMixin():
    """The DistanceFilterViewSetMixin."""

    filter_backends = (
        DistanceToPointFilter,
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
        OwnerFilter,
    )
    bbox_filter_include_overlapping = True
    distance_filter_convert_meters = True
    distance_filter_field = "location"
