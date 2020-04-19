"""The users managers module."""
from typing import TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from location.repositories import CountryRepository

from .repositories import GroupRepository

if TYPE_CHECKING:
    from .models import User, UserLanguage, UserLocation


class UserSettingsManager(models.Manager):
    """The user settings manager."""

    def get_list(self) -> QuerySet:
        """Return a list of user contacts."""
        return self.all().select_related(
            'user',
            'created_by',
            'modified_by',
        )

    def update_or_create_from_user_language(
        self,
        user_language: 'UserLanguage',
    ):
        """Update or create an user settings from the user language object."""
        settings, created = self.get_or_create(user=user_language.user)
        if created or not settings.language:
            settings.language = user_language.language
            try:
                settings.full_clean()
                settings.save()
            except ValidationError:
                pass

    def update_or_create_from_user_location(
        self,
        user_location: 'UserLocation',
    ):
        """Update or create an user settings from the user location object."""
        country = user_location.country
        if not country:
            return
        settings, created = self.get_or_create(user=user_location.user)

        def save(settings):
            try:
                settings.full_clean()
                settings.save()
            except ValidationError:
                pass

        if country.language_codes and (created or not settings.language):
            settings.language = CountryRepository.get_language(country)
            save(settings)

        if country.currency and (created or not settings.currency):
            settings.currency = country.currency
            save(settings)


class UserContactManager(models.Manager):
    """The user contact manager."""

    def get_list(self) -> QuerySet:
        """Return a list of user contacts."""
        return self.all().select_related(
            'user',
            'created_by',
            'modified_by',
        )


class UserLanguageManager(models.Manager):
    """The user language manager."""

    def get_list(self) -> QuerySet:
        """Return a list of user languages."""
        return self.all().select_related(
            'user',
            'created_by',
            'modified_by',
        )


class UserLocationManager(models.Manager):
    """The user location manager."""

    def get_list(self) -> QuerySet:
        """Return a list of user locations."""
        return self.all().select_related(
            'country',
            'region',
            'subregion',
            'city',
            'district',
            'postal_code',
            'user',
            'created_by',
            'modified_by',
        )


class UserManager(BaseUserManager):
    """
    The user model manager.

    The user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(
            self,
            email: str,
            password: str,
            **extra_fields,
    ) -> 'User':
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('The email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        group = GroupRepository().get_or_create_user_group()
        group.user_set.add(user)

        return user

    def create_superuser(
            self,
            email: str,
            password: str,
            **extra_fields,
    ) -> 'User':
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)
