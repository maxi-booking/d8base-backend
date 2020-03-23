"""The users views module."""
from rest_framework import viewsets

from .models import UserLanguage, UserLocation
from .serializers import UserLanguageSerializer, UserLocationSerializer


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
