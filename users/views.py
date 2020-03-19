"""The users views module."""
from rest_framework import viewsets

from .models import UserLanguage
from .serializers import UserLanguageSerializer


class UserLanguageViewSet(viewsets.ModelViewSet):
    """The Continent viewset."""

    is_owner_filter_enabled = True
    serializer_class = UserLanguageSerializer
    queryset = UserLanguage.objects.all()
