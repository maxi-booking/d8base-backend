"""The services validators module."""
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .models import Price, ServiceLocation


def validate_service_location(location: 'ServiceLocation'):
    """Validate the service location."""
    if location.service.professional != location.location.professional:
        raise ValidationError(
            {'location': _('Location from the other professional.')})


def validate_service_price(price: 'Price'):
    """Validate the service price."""
    if price.is_price_fixed and not price.price:
        raise ValidationError({'price': _('The price must be specified.')})

    if not price.is_price_fixed:
        if not price.start_price or not price.end_price:
            raise ValidationError({
                'price': _('The starting and ending prices must be specified.')
            })
        if price.start_price.currency != price.end_price.currency:
            raise ValidationError(
                {'start_price': _('The prices must have the same currency.')})

        if price.start_price > price.end_price:
            raise ValidationError({
                'start_price':
                    _('The starting price must be less than the ending price.')
            })
