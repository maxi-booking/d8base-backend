"""The orders managers module."""
from typing import TYPE_CHECKING

from django.db import models
from django.db.models.query import QuerySet

if TYPE_CHECKING:
    from .models import Order


class OrdersManager(models.Manager):
    """The orders slot manager."""

    def get_list(self) -> QuerySet:
        """Return a list of objects."""
        return self.all().select_related(
            "service",
            "service__professional",
            "service__professional__user",
            "created_by",
            "modified_by",
            "client",
        )

    def get_overlapping_entries(
        self,
        order: "Order",
    ) -> QuerySet:
        """Return the overlapping entries."""
        query = self.get_list().filter(
            start_datetime__lt=order.end_datetime,
            end_datetime__gt=order.start_datetime,
            service__professional__user=order.service.professional.user,
        )
        if order.pk:
            query = query.exclude(pk=order.pk)
        return query
