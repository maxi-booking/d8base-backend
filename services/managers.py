"""The services managers module."""
from django.db import models
from django.db.models.query import QuerySet


class ServiceManager(models.Manager):
    """The service manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            'professional__user',
            'professional',
            'created_by',
            'modified_by',
        )


class ServiceTagManager(models.Manager):
    """The service tag manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            'service',
            'created_by',
            'modified_by',
        )


class ServiceLocationManager(models.Manager):
    """The service location manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            'service',
            'created_by',
            'modified_by',
        )


class ServicePhotoManager(models.Manager):
    """The service photo manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            'service',
            'created_by',
            'modified_by',
        )


class ServicePriceManager(models.Manager):
    """The service price manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            'service',
            'created_by',
            'modified_by',
        )
