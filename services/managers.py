"""The services managers module."""
from django.db import models
from django.db.models.query import QuerySet

from users.models import User


class ServiceManager(models.Manager):
    """The service manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            'professional__user',
            'professional',
            'price',
            'created_by',
            'modified_by',
        )

    def get_user_list(self, user: User) -> QuerySet:
        """Return a list of services filtered by user."""
        return self.get_list().filter(professional__user=user)


class ServiceTagManager(models.Manager):
    """The service tag manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            'service__professional',
            'service__professional__user',
            'service',
            'created_by',
            'modified_by',
        )

    def get_names(self) -> QuerySet:
        """Return a list of professional tags names."""
        return self.all().distinct('name').order_by('name').values('name')


class ServiceLocationManager(models.Manager):
    """The service location manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            'service__professional',
            'service__professional__user',
            'service',
            'created_by',
            'modified_by',
        )


class ServicePhotoManager(models.Manager):
    """The service photo manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            'service__professional',
            'service__professional__user',
            'service',
            'created_by',
            'modified_by',
        )


class ServicePriceManager(models.Manager):
    """The service price manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            'service__professional',
            'service__professional__user',
            'service',
            'created_by',
            'modified_by',
        )
