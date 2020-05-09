"""The professionals validators module."""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_user_location(obj):
    """Validate the user location."""
    if obj.user_location and\
            obj.user_location.user != obj.professional.user:
        raise ValidationError(
            {'user_location': _('User location from the another user.')})
