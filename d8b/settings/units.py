"""The units settings module."""
from django.utils.translation import gettext_lazy as _

UNITS_METRIC = 0
UNITS_IMPERIAL = 1
UNITS = ((UNITS_METRIC, _('metric')), (UNITS_IMPERIAL, _('imperial/US')))
IMPERIAL_UNITS_COUNTRIES = ('us', 'mm', 'lr')
