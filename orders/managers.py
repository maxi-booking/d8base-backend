"""The orders managers module."""
from typing import TYPE_CHECKING, Optional

import arrow
from django.db import models
from django.db.models.query import QuerySet

if TYPE_CHECKING:
    from .models import Order
    from professionals.models import Professional
    from services.models import Service


class OrdersManager(models.Manager):
    """The orders slot manager."""

    def get_list(self) -> "QuerySet[Order]":
        """Return a list of objects."""
        return self.all().select_related(
            "service",
            "service_location",
            "client_location",
            "service__professional",
            "service__professional__user",
            "client",
            "client__settings",
            "created_by",
            "modified_by",
        ).prefetch_related("client__languages")

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

    def get_between_dates(
        self,
        start: arrow.Arrow,
        end: arrow.Arrow,
        professional: "Professional",
        service: Optional["Service"] = None,
    ) -> QuerySet:
        """Return between the dates."""
        if service and service.is_enabled:
            services = [service]
        else:
            services = professional.services.all()
        query = self.filter(
            service__in=services,
            start_datetime__lte=end.datetime,
            end_datetime__gte=start.datetime,
        )

        return query
