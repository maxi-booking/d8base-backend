"""The users models module."""
from typing import List

from cities.models import (City, Country, District, PostalCode, Region,
                           Subregion)
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from d8b.fields import LanguageField
from d8b.models import CommonInfo
from location.services import LocationAutofiller

from .managers import UserManager
from .validators import validate_birthday


class User(AbstractUser):
    """The user class."""

    ACCOUNT_USER: str = 'user'
    ACCOUNT_SPECIALIST: str = 'specialist'
    ACCOUNT_CHOICES = [
        (ACCOUNT_USER, 'user'),
        (ACCOUNT_SPECIALIST, 'specialist'),
    ]

    GENDER_MALE: int = 0
    GENDER_FEMALE: int = 1
    GENDER_CHOICES = [(GENDER_MALE, _('male')), (GENDER_FEMALE, _('female'))]

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = []

    objects: UserManager = UserManager()

    username = None
    email = models.EmailField(_('email'), unique=True)
    patronymic = models.CharField(
        _('patronymic'),
        max_length=150,
        blank=True,
        null=True,
    )
    phone = PhoneNumberField(blank=True, null=True)
    gender = models.PositiveIntegerField(
        _('gender'),
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
    birthday = models.DateField(
        _('birthday'),
        blank=True,
        null=True,
        validators=[validate_birthday],
    )
    account_type = models.CharField(
        _('account type'),
        max_length=10,
        choices=ACCOUNT_CHOICES,
        default=ACCOUNT_USER,
    )

    # avatar

    def __str__(self):
        """Return a string representation of the object."""
        return self.email


class UserLocation(CommonInfo):
    """The user location class."""

    autofiller = LocationAutofiller

    country = models.ForeignKey(
        Country,
        verbose_name=_('country'),
        on_delete=models.CASCADE,
        related_name='user_locations',
    )
    region = models.ForeignKey(
        Region,
        verbose_name=_('region'),
        on_delete=models.SET_NULL,
        related_name='user_locations',
        null=True,
        blank=True,
    )
    subregion = models.ForeignKey(
        Subregion,
        verbose_name=_('subregion'),
        on_delete=models.SET_NULL,
        related_name='user_locations',
        null=True,
        blank=True,
    )
    city = models.ForeignKey(
        City,
        verbose_name=_('city'),
        on_delete=models.SET_NULL,
        related_name='user_locations',
        null=True,
        blank=True,
    )
    district = models.ForeignKey(
        District,
        verbose_name=_('district'),
        on_delete=models.SET_NULL,
        related_name='user_locations',
        null=True,
        blank=True,
    )
    postal_code = models.ForeignKey(
        PostalCode,
        verbose_name=_('postal code'),
        on_delete=models.SET_NULL,
        related_name='user_locations',
        null=True,
        blank=True,
    )
    address = models.CharField(
        _('address'),
        max_length=255,
        null=True,
        blank=True,
    )
    coordinates = gis_models.PointField(
        _('coordinates'),
        null=True,
        blank=True,
    )
    is_default = models.BooleanField(
        default=False,
        help_text=_('is default location?'),
        verbose_name=_('is default'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='locations',
        verbose_name=_('user'),
    )

    def save(self, **kwargs):
        """Save the object."""
        self.autofiller(self).autofill_location()
        super().save(**kwargs)

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.user}: {self.country}, {self.city}, {self.address}'

    class Meta:
        """The user location class META class."""

        ordering = ('-created', )


class UserLanguage(CommonInfo):
    """The user language class."""

    language = LanguageField(verbose_name=_('language'))
    is_native = models.BooleanField(
        default=True,
        help_text=_('is native language?'),
        verbose_name=_('is native'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='languages',
        verbose_name=_('user'),
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.user}: {self.language}'

    class Meta:
        """The user language class META class."""

        ordering = ('language', )
        unique_together = (('language', 'user'), )
