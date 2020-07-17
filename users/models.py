"""The users models module."""
from typing import List

from cities.models import Country
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import CurrencyField
from djmoney.settings import CURRENCY_CHOICES
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import SmartResize
from phonenumber_field.modelfields import PhoneNumberField

from contacts.models import ContactMixin
from d8b.fields import LanguageField, UnitsField
from d8b.models import CommonInfo
from d8b.services import DefaultFieldSetter, RandomFilenameGenerator
from location.models import LocationMixin
from location.services import LocationAutofiller

from .managers import (UserContactManager, UserLanguageManager,
                       UserLocationManager, UserManager,
                       UserSavedProfessionalManager, UserSettingsManager)
from .validators import validate_birthday


class CalculatedUserUnits:
    """The calculated user units."""


class User(AbstractUser):
    """The user class."""

    ACCOUNT_USER: str = "user"
    ACCOUNT_PROFESSIONAL: str = "professional"
    ACCOUNT_CHOICES = [
        (ACCOUNT_USER, _("user")),
        (ACCOUNT_PROFESSIONAL, _("professional")),
    ]

    GENDER_MALE: int = 0
    GENDER_FEMALE: int = 1
    GENDER_CHOICES = [(GENDER_MALE, _("male")), (GENDER_FEMALE, _("female"))]

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = []

    objects: UserManager = UserManager()

    username = None
    email = models.EmailField(
        _("email"),
        unique=True,
        db_index=True,
    )
    patronymic = models.CharField(
        _("patronymic"),
        max_length=150,
        blank=True,
        null=True,
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        db_index=True,
    )
    gender = models.PositiveIntegerField(
        _("gender"),
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
    birthday = models.DateField(
        _("birthday"),
        blank=True,
        null=True,
        validators=[validate_birthday],
    )
    nationality = models.ForeignKey(
        Country,
        verbose_name=_("nationality"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="nationalities",
    )
    account_type = models.CharField(
        _("account type"),
        max_length=20,
        choices=ACCOUNT_CHOICES,
        default=ACCOUNT_USER,
    )
    is_confirmed = models.BooleanField(
        default=False,
        help_text=_("is account confirmed?"),
        verbose_name=_("is confirmed"),
    )
    avatar = ProcessedImageField(
        blank=True,
        null=True,
        upload_to=RandomFilenameGenerator("avatars", "email"),
        processors=[
            SmartResize(
                width=settings.D8B_AVATAR_WIDTH,
                height=settings.D8B_AVATAR_HEIGHT,
                upscale=True,
            )
        ],
        format="PNG",
    )

    avatar_thumbnail = ImageSpecField(
        source="avatar",
        processors=[
            SmartResize(
                width=settings.D8B_AVATAR_THUMBNAIL_WIDTH,
                height=settings.D8B_AVATAR_THUMBNAIL_HEIGHT,
            )
        ],
        format="PNG",
    )

    @property
    def preferred_language(self) -> str:
        """Get the user prefferred language."""
        try:
            # pylint: disable=no-member
            return self.settings.language
        except UserSettings.DoesNotExist:
            return settings.LANGUAGE_CODE

    def __str__(self):
        """Return a string representation of the object."""
        return self.email


class UserSavedProfessional(CommonInfo):
    """The user saved professional class."""

    objects = UserSavedProfessionalManager()

    note = models.CharField(
        _("note"),
        null=True,
        blank=True,
        max_length=255,
    )
    professional = models.ForeignKey(
        "professionals.Professional",
        on_delete=models.CASCADE,
        related_name="user_saved_professionals",
        verbose_name=_("professional"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_professionals",
        verbose_name=_("user"),
    )

    class Meta(CommonInfo.Meta):
        """The user language class META class."""

        abstract = False
        unique_together = (("user", "professional"), )

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.user}: {self.professional} saved professional"


class UserSettings(CommonInfo):
    """The user settings class."""

    objects = UserSettingsManager()

    language = LanguageField(
        verbose_name=_("language"),
        null=True,
        blank=True,
        default=settings.LANGUAGE_CODE,
        choices=settings.APP_LANGUAGES,
    )
    currency = CurrencyField(
        verbose_name=_("currency"),
        null=True,
        blank=True,
        choices=CURRENCY_CHOICES,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="settings",
        verbose_name=_("user"),
    )
    is_last_name_hidden = models.BooleanField(
        default=False,
        help_text=_("Is the last name hidden from other users?"),
        verbose_name=_("is the last name hidden?"),
    )
    units = UnitsField(verbose_name=_("units"))

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.user} settings"


class UserLocation(CommonInfo, LocationMixin):
    """The user location class."""

    objects = UserLocationManager()
    default_field_setter = DefaultFieldSetter
    autofiller = LocationAutofiller

    is_default = models.BooleanField(
        default=False,
        help_text=_("is default location?"),
        verbose_name=_("is default"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="locations",
        verbose_name=_("user"),
    )

    def save(self, **kwargs):
        """Save the object."""
        self.autofiller(self).autofill_location()
        self.default_field_setter(self).\
            process_default_for_query(user=self.user)
        super().save(**kwargs)
        UserSettings.objects.update_or_create_from_user_location(self)

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.user}: " + ", ".join(
            map(str, filter(None, [self.country, self.city, self.address])))

    class Meta(CommonInfo.Meta):
        """The user location class META class."""

        abstract = False


class UserLanguage(CommonInfo):
    """The user language class."""

    objects = UserLanguageManager()

    language = LanguageField(verbose_name=_("language"))
    is_native = models.BooleanField(
        default=True,
        help_text=_("is native language?"),
        verbose_name=_("is native"),
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="languages",
        verbose_name=_("user"),
    )

    def save(self, **kwargs):
        """Save the object."""
        super().save(**kwargs)
        UserSettings.objects.update_or_create_from_user_language(self)

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.user}: {self.language}"

    class Meta:
        """The user language class META class."""

        ordering = ("language", )
        unique_together = (("language", "user"), )


class UserContact(ContactMixin, CommonInfo):
    """The user contact class."""

    objects = UserContactManager()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="contacts",
        verbose_name=_("user"),
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.user}: {self.contact} {self.value}"

    class Meta(CommonInfo.Meta):
        """The user contact class META class."""

        abstract = False
        unique_together = (("value", "user", "contact"), )
