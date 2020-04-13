"""The professionals views module."""
from rest_framework import viewsets
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from d8b.viewsets import AllowAnyViewSetMixin

from .models import Category, Subcategory
from .serializers import CategorySerializer, SubcategorySerializer


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
