"""The users models module."""
from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from d8b.fields import LanguageField
from d8b.models import CommonInfo

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

    # --- location
    # country
    # region
    # city
    # postal code
    # address
    # coordinates
    # --- location

    def __str__(self):
        """Return a string representation of the object."""
        return self.email


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

    class Meta:
        """The user language class META class."""

        ordering = ('language', )
        unique_together = (('language', 'user'), )
