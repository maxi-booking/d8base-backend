"""The users views module."""
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_registration.utils.verification_notifications import \
    send_register_verification_email_notification

from d8b.units import is_imperial_units

from .interfaces import UserCalculatedUnits
from .models import (UserContact, UserLanguage, UserLocation,
                     UserSavedProfessional, UserSettings)
from .serializers import (UserCalculatedUnitsSerializer, UserContactSerializer,
                          UserLanguageSerializer, UserLocationSerializer,
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


# TODO: test it
class UserCalculatedUnitsViewSet(viewsets.ViewSet):
    """The user calculated units viewset."""

    serializer_class = UserCalculatedUnitsSerializer
    permission_classes = (AllowAny, )

    def list(self, request):
        """Return units."""
        is_imperial = is_imperial_units(request.user)

        units = UserCalculatedUnits(
            is_imperial_units=is_imperial,
            distance='mi' if is_imperial else 'km',
            timezone=timezone.get_current_timezone_name(),
        )
        serializer = self.serializer_class(instance=units, many=False)
        return Response(serializer.data)


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
