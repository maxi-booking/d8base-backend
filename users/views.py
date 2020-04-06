"""The users views module."""
from rest_framework import viewsets

from .models import UserContact, UserLanguage, UserLocation
from .serializers import (UserContactSerializer, UserLanguageSerializer,
                          UserLocationSerializer)


class UserLanguageViewSet(viewsets.ModelViewSet):
    """The user languages viewset."""

    is_owner_filter_enabled = True
    serializer_class = UserLanguageSerializer
    queryset = UserLanguage.objects.get_list()


class UserLocationViewSet(viewsets.ModelViewSet):
    """The user locations viewset."""

    is_owner_filter_enabled = True
    serializer_class = UserLocationSerializer
    queryset = UserLocation.objects.get_list()


class UserContactViewSet(viewsets.ModelViewSet):
    """The user contacts viewset."""

    is_owner_filter_enabled = True
    serializer_class = UserContactSerializer
    queryset = UserContact.objects.get_list()
