"""The location models module."""
from dataclasses import dataclass

from cities.models import (City, Country, District, PostalCode, Region,
                           Subregion)
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.translation import gettext_lazy as _

from d8b.fields import TimezoneField, UnitsField


@dataclass
class Language():
    """The language model class."""

    code: str
    name: str


class LocationMixin(models.Model):
    """The location mixin."""

    country = models.ForeignKey(
        Country,
        verbose_name=_('country'),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='%(class)s_locations',
    )
    region = models.ForeignKey(
        Region,
        verbose_name=_('region'),
        on_delete=models.SET_NULL,
        related_name='%(class)s_locations',
        null=True,
        blank=True,
    )
    subregion = models.ForeignKey(
        Subregion,
        verbose_name=_('subregion'),
        on_delete=models.SET_NULL,
        related_name='%(class)s_locations',
        null=True,
        blank=True,
    )
    city = models.ForeignKey(
        City,
        verbose_name=_('city'),
        on_delete=models.SET_NULL,
        related_name='%(class)s_locations',
        null=True,
        blank=True,
    )
    district = models.ForeignKey(
        District,
        verbose_name=_('district'),
        on_delete=models.SET_NULL,
        related_name='%(class)s_locations',
        null=True,
        blank=True,
    )
    postal_code = models.ForeignKey(
        PostalCode,
        verbose_name=_('postal code'),
        on_delete=models.SET_NULL,
        related_name='%(class)s_locations',
        null=True,
        blank=True,
    )
    address = models.CharField(
        verbose_name=_('address'),
        max_length=255,
        null=True,
        blank=True,
    )
    coordinates = gis_models.PointField(
        verbose_name=_('coordinates'),
        null=True,
        blank=True,
    )
    units = UnitsField(verbose_name=_('units'))
    timezone = TimezoneField(
        verbose_name=_('timezone'),
        null=True,
        blank=True,
    )

    class Meta():
        """The location mixin class META class."""

        abstract = True
