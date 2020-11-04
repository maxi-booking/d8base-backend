"""The services managers module."""
from typing import TYPE_CHECKING, List, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Min
from django.db.models.query import QuerySet

from users.models import User

if TYPE_CHECKING:
    from services.models import Service
    from professionals.models import Professional


class ServiceManager(models.Manager):
    """The service manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            "professional__user",
            "professional",
            "price",
            "created_by",
            "modified_by",
        )

    def get_extended_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.get_list().prefetch_related(
            "tags",
            "locations",
        )

    def get_user_list(self, user: User) -> QuerySet:
        """Return a list of services filtered by user."""
        return self.get_list().filter(professional__user=user)

    def get_by_params(self, **kwargs) -> Optional["Service"]:
        """Return an object by a pk."""
        try:
            return self.select_related(
                "professional__user",
                "professional",
                "price",
                "created_by",
                "modified_by",
            ).get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def get_min_duration(self, professional: "Professional") -> int:
        """Get the minimum duration of the professional services."""
        result = self.filter(
            professional=professional,
            is_enabled=True,
        ).aggregate(Min("duration"))["duration__min"]
        return result or 0

    def get_for_avaliability_generation(
        self,
        ids: Optional[List[int]] = None,
    ) -> QuerySet:
        """Return a list of services for availability generation."""
        query = self.get_list().filter(is_base_schedule=False)
        if not ids:
            return query
        return query.filter(pk__in=ids)


class ServiceTagManager(models.Manager):
    """The service tag manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            "service__professional",
            "service__professional__user",
            "service",
            "created_by",
            "modified_by",
        )

    def get_names(self) -> QuerySet:
        """Return a list of professional tags names."""
        return self.all().distinct("name").order_by("name").values("name")


class ServiceLocationManager(models.Manager):
    """The service location manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            "service__professional",
            "service__professional__user",
            "service",
            "created_by",
            "modified_by",
        )


class ServicePhotoManager(models.Manager):
    """The service photo manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            "service__professional",
            "service__professional__user",
            "service",
            "created_by",
            "modified_by",
        )


class ServicePriceManager(models.Manager):
    """The service price manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            "service__professional",
            "service__professional__user",
            "service",
            "created_by",
            "modified_by",
        )
