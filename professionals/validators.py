"""The professionals validators module."""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# TODO: test it
def validate_user_location(self):
    """Validate the user location."""
    if self.user_location and\
            self.user_location.user != self.professional.user:
        raise ValidationError(
            {'user_location': _('User location from the another user.')})
