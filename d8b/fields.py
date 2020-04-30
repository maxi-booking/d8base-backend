"""The d8b fields module."""
from django.conf import settings
from django.db.models.fields import CharField, PositiveSmallIntegerField
from django.utils.translation import gettext_lazy as _
from pytz import common_timezones


class LanguageField(CharField):
    """The language field for Django models."""

    description = _('Language code')

    def __init__(self, *args, **kwargs):
        """Initialize the object."""
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', settings.LANGUAGES)
        super().__init__(*args, **kwargs)


class UnitsField(PositiveSmallIntegerField):
    """The units of measurement field for Django models."""

    description = _('Units')

    def __init__(self, *args, **kwargs):
        """Initialize the object."""
        kwargs.setdefault('choices', settings.UNITS)
        kwargs.setdefault('default', settings.UNITS_METRIC)
        super().__init__(*args, **kwargs)


class TimezoneField(CharField):
    """The timezone field for Django models."""

    description = _('Timezone')

    def __init__(self, *args, **kwargs):
        """Initialize the object."""
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('choices', zip(common_timezones, common_timezones))
        super().__init__(*args, **kwargs)
