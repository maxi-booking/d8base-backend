"""The contacts views module."""
from rest_framework import viewsets
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .filters import ContactFilter
from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(
        CacheResponseMixin,
        viewsets.ReadOnlyModelViewSet,
):
    """The contact viewset."""

    serializer_class = ContactSerializer
    queryset = Contact.objects.get_list()
    search_fields = ('=id', 'name')
    filterset_class = ContactFilter
