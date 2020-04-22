"""The professionals views module."""
from rest_framework import viewsets
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from d8b.viewsets import AllowAnyViewSetMixin

from .filtersets import ProfessionalTagFilterSet
from .models import Category, Professional, ProfessionalTag, Subcategory
from .serializers import (CategorySerializer, ProfessionalSerializer,
                          ProfessionalTagListSerializer,
                          ProfessionalTagSerializer, SubcategorySerializer)


class ProfessionalTagViewSet(viewsets.ModelViewSet):
    """The professional tag viewset."""

    is_owner_filter_enabled = True
    owner_filter_field = 'professional__user'
    serializer_class = ProfessionalTagSerializer
    queryset = ProfessionalTag.objects.get_list()
    search_fields = ('=id', 'name')
    filterset_class = ProfessionalTagFilterSet


class ProfessionalTagListViewSet(viewsets.ReadOnlyModelViewSet):
    """The professional tag list viewset."""

    serializer_class = ProfessionalTagListSerializer
    queryset = ProfessionalTag.objects.get_names()
    search_fields = ('name', )


class ProfessionalViewSet(viewsets.ModelViewSet):
    """The professional viewset."""

    is_owner_filter_enabled = True
    serializer_class = ProfessionalSerializer
    queryset = Professional.objects.get_list()
    search_fields = ('=id', 'name')


class CategoryViewSet(
        CacheResponseMixin,
        AllowAnyViewSetMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The category viewset."""

    serializer_class = CategorySerializer
    queryset = Category.objects.get_list()
    search_fields = ('=id', 'name')


class SubcategoryViewSet(
        CacheResponseMixin,
        AllowAnyViewSetMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The subcategory viewset."""

    serializer_class = SubcategorySerializer
    queryset = Subcategory.objects.get_list()
    search_fields = ('=id', 'name', 'category__name')
    filterset_fields = ('category', )
