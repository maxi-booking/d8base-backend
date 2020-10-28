"""The contacts models module."""
from cities.models import Country
from django.db import models
from django.utils.translation import gettext_lazy as _

from d8b.models import CommonInfo

from .managers import ContactsManager


class Contact(CommonInfo):
    """The user contact class."""

    objects = ContactsManager()

    name = models.CharField(
        _("name"),
        max_length=150,
        blank=True,
        null=True,
        db_index=True,
    )
    code = models.CharField(
        _("code"),
        max_length=150,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )
    is_default = models.BooleanField(
        _("is_default"),
        default=False,
        help_text=_("Does the contact appear in the default list?"),
    )
    countries = models.ManyToManyField(
        Country,
        blank=True,
        verbose_name=_("country"),
        related_name="contacts",
    )
    excluded_countries = models.ManyToManyField(
        Country,
        blank=True,
        verbose_name=_("excluded countries"),
        related_name="contacts_excluded",
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.name}"

    class Meta:
        """The contact class META class."""

        ordering = ("name", )


class ContactMixin(models.Model):
    """The contact mixin class."""

    value = models.CharField(
        verbose_name=_("value"),
        max_length=255,
        db_index=True,
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_contacts",
        verbose_name=_("contact"),
    )

    @property
    def contact_display(self) -> str:
        """Return the name of the contact."""
        return self.contact.name

    @property
    def contact_code(self) -> str:
        """Return the code of the contact."""
        return self.contact.code

    class Meta():
        """The contact mixin class META class."""

        abstract = True
