"""The users views module."""
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_registration.utils.verification_notifications import \
    send_register_verification_email_notification

from .models import (UserContact, UserLanguage, UserLocation,
                     UserSavedProfessional, UserSettings)
from .serializers import (UserContactSerializer, UserLanguageSerializer,
                          UserLocationSerializer,
                          UserSavedProfessionalSerializer,
                          UserSettingsSerializer)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resend_verify_registration(request):
    """Resend a registration verification email."""
    user = request.user
    if user.is_confirmed:
        raise NotFound('the user has already been confirmed')
    send_register_verification_email_notification(request, request.user)
    return Response({'detail': 'a message has been sent'})


class UserSettingsViewSet(viewsets.ModelViewSet):
    """The user settings viewset."""

    is_owner_filter_enabled = True
    serializer_class = UserSettingsSerializer
    queryset = UserSettings.objects.get_list()


class UserSavedProfessionalViewSet(viewsets.ModelViewSet):
    """The user saved professional viewset."""

    is_owner_filter_enabled = True
    serializer_class = UserSavedProfessionalSerializer
    queryset = UserSavedProfessional.objects.get_list()


class UserLanguageViewSet(viewsets.ModelViewSet):
    """The user languages viewset."""

    is_owner_filter_enabled = True
    serializer_class = UserLanguageSerializer
    queryset = UserLanguage.objects.get_list()


class UserLocationViewSet(viewsets.ModelViewSet):
    """The user locations viewset."""

    is_owner_filter_enabled = True
    serializer_class = UserLocationSerializer
    filterset_fields = ('is_default', )
    queryset = UserLocation.objects.get_list()


class UserContactViewSet(viewsets.ModelViewSet):
    """The user contacts viewset."""

    is_owner_filter_enabled = True
    serializer_class = UserContactSerializer
    queryset = UserContact.objects.get_list()
    filterset_fields = ('contact', )
