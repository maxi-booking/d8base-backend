"""The contacts models module."""
from cities.models import Country
from django.db import models
from django.utils.translation import ugettext_lazy as _

from d8b.models import CommonInfo

from .managers import ContactsManager


class Contact(CommonInfo):
    """The user language class."""

    objects = ContactsManager()

    name = models.CharField(
        _('name'),
        max_length=150,
        blank=True,
        null=True,
    )
    countries = models.ManyToManyField(
        Country,
        blank=True,
        verbose_name=_('country'),
        related_name='contacts',
    )
    excluded_countries = models.ManyToManyField(
        Country,
        blank=True,
        verbose_name=_('excluded countries'),
        related_name='contacts_excluded',
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.name}'

    class Meta:
        """The contact class META class."""

        ordering = ('name', )
