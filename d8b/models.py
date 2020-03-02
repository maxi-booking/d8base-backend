"""The d8b models module."""
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from users.models import User

from .middleware import ThreadSafeUserMiddleware


class CommonInfo(TimeStampedModel):
    """The abstract model with common info."""

    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
        verbose_name=_('created by'),
        related_name="%(app_label)s_%(class)s_created_by")

    modified_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
        editable=False,
        verbose_name=_('modified by'),
        related_name="%(app_label)s_%(class)s_modified_by")

    @staticmethod
    def get_current_user() -> Optional[User]:
        """
        Get the currently logged in user over middleware.

        Can be overwritten to use e.g. other middleware or additional
        functionality.
        """
        return ThreadSafeUserMiddleware.get_current_user()

    def _set_user_fields(self, user: Optional[User]) -> None:
        """
        Set user-related fields before saving the instance.

        If no user with primary key is given the fields are not set.
        """
        if not user or not user.pk:
            return None

        if not self.pk:
            self.created_by = user
        self.modified_by = user
        return None

    def save(self, **kwargs) -> None:
        """Save the object."""
        self._set_user_fields(self.get_current_user())
        super(CommonInfo, self).save(**kwargs)

    class Meta:
        """The metainformation."""

        abstract = True
