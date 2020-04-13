"""The users models module."""
from typing import List

from cities.models import (City, Country, District, PostalCode, Region,
                           Subregion)
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import SmartResize
from phonenumber_field.modelfields import PhoneNumberField

from contacts.models import Contact
from d8b.fields import LanguageField, TimezoneField, UnitsField
from d8b.models import CommonInfo
from d8b.services import DefaultFieldSetter, RandomFilenameGenerator
from location.services import LocationAutofiller

from .managers import (UserContactManager, UserLanguageManager,
                       UserLocationManager, UserManager)
from .validators import validate_birthday


class User(AbstractUser):
    """The user class."""

    ACCOUNT_USER: str = 'user'
    ACCOUNT_PROFESSIONAL: str = 'professional'
    ACCOUNT_CHOICES = [
        (ACCOUNT_USER, 'user'),
        (ACCOUNT_PROFESSIONAL, 'professional'),
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
    avatar = ProcessedImageField(
        blank=True,
        null=True,
        upload_to=RandomFilenameGenerator('avatars', 'email'),
        processors=[
            SmartResize(
                width=settings.D8B_AVATAR_WIDTH,
                height=settings.D8B_AVATAR_HEIGHT,
                upscale=True,
            )
        ],
        format='PNG',
    )

    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[
            SmartResize(
                width=settings.D8B_AVATAR_THUMBNAIL_WIDTH,
                height=settings.D8B_AVATAR_THUMBNAIL_HEIGHT,
            )
        ],
        format='PNG',
    )

    def __str__(self):
        """Return a string representation of the object."""
        return self.email


class UserLocation(CommonInfo):
    """The user location class."""

    autofiller = LocationAutofiller
    default_field_setter = DefaultFieldSetter
    objects = UserLocationManager()

    country = models.ForeignKey(
        Country,
        verbose_name=_('country'),
        null=True,
        blank=True,
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
    is_default = models.BooleanField(
        default=False,
        help_text=_('is default location?'),
        verbose_name=_('is default'),
    )
    units = UnitsField(verbose_name=_('units'))
    timezone = TimezoneField(
        verbose_name=_('timezone'),
        null=True,
        blank=True,
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
        self.default_field_setter(self).\
            process_default_for_query(user=self.user)
        super().save(**kwargs)

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.user}: ' + ', '.join(
            map(str, filter(None, [self.country, self.city, self.address])))

    class Meta:
        """The user location class META class."""

        ordering = ('-created', )


class UserLanguage(CommonInfo):
    """The user language class."""

    objects = UserLanguageManager()

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


class UserContact(CommonInfo):
    """The user contact class."""

    objects = UserContactManager()

    value = models.CharField(
        verbose_name=_('value'),
        max_length=255,
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='user_contacts',
        verbose_name=_('contact'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name=_('user'),
    )

    @property
    def contact_display(self) -> str:
        """Return the name of the contact."""
        return self.contact.name

    def __str__(self) -> str:
        """Return the string representation."""
        return f'{self.user}: {self.contact} {self.value}'

    class Meta:
        """The user language class META class."""

        unique_together = (('value', 'user', 'contact'), )
