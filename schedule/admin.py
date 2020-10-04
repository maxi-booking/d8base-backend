"""The schedule admin module."""
from typing import Any, List

from django.contrib import admin
from reversion.admin import VersionAdmin

from d8b.admin import (FieldsetFieldsUpdateMixin, ListDisplayUpdateMixin,
                       ListFilterUpdateMixin, ListLinksUpdateMixin)
from professionals.models import Professional

from .admin_fiters import ProfessionalFilter, ServiceFilter
from .models import (AvailabilitySlot, ProfessionalClosedPeriod,
                     ProfessionalSchedule, ServiceClosedPeriod,
                     ServiceSchedule)


class ClosedPeriodMixin(VersionAdmin):
    """The closed period mixin admin class."""

    list_display = [
        "id", "start_datetime", "end_datetime", "is_enabled", "created",
        "modified"
    ]
    list_display_links = ["id"]
    readonly_fields = ("created", "modified", "created_by", "modified_by")
    list_filter = ("start_datetime", "end_datetime", "is_enabled")

    fieldsets = [
        ("General", {
            "fields": ["start_datetime", "end_datetime"]
        }),
        ("Options", {
            "fields": [
                "is_enabled", "created", "modified", "created_by",
                "modified_by"
            ]
        }),
    ]

    class Media:
        """Required for the AutocompleteFilter."""


class ScheduleMixin(VersionAdmin):
    """The schedule mixin admin class."""

    list_display = [
        "id", "day_of_week", "start_time", "end_time", "timezone",
        "is_enabled", "created", "modified"
    ]
    list_display_links = ["id"]
    readonly_fields = (
        "created",
        "modified",
        "created_by",
        "modified_by",
    )
    list_filter = ("day_of_week", "is_enabled")

    fieldsets = [
        ("General", {
            "fields": ["day_of_week", "start_time", "end_time", "timezone"]
        }),
        ("Options", {
            "fields": [
                "is_enabled", "created", "modified", "created_by",
                "modified_by"
            ]
        }),
    ]

    class Media:
        """Required for the AutocompleteFilter."""


@admin.register(ProfessionalSchedule)
class ProfessionalScheduleAdmin(
        ScheduleMixin,
        ListFilterUpdateMixin,
        ListDisplayUpdateMixin,
        ListLinksUpdateMixin,
        FieldsetFieldsUpdateMixin,
):
    """The professional schedule admin class."""

    list_filter_extend: List[Any] = [ProfessionalFilter]
    list_filter_remove: List[Any] = []

    list_display_extend: List[Any] = ["professional"]
    list_display_remove: List[Any] = []

    list_links_extend: List[Any] = ["professional"]
    list_links_remove: List[Any] = []

    fieldsets_fields_extend: List[Any] = ["professional"]
    fieldsets_fields_remove: List[Any] = []

    autocomplete_fields = ("professional", )
    list_select_related = ("professional", "professional__user")


@admin.register(ServiceSchedule)
class ServiceScheduleAdmin(
        ScheduleMixin,
        ListFilterUpdateMixin,
        ListDisplayUpdateMixin,
        ListLinksUpdateMixin,
        FieldsetFieldsUpdateMixin,
):
    """The service schedule admin class."""

    list_filter_extend: List[Any] = [ServiceFilter]
    list_filter_remove: List[Any] = []

    list_display_extend: List[Any] = ["service"]
    list_display_remove: List[Any] = []

    list_links_extend: List[Any] = ["service"]
    list_links_remove: List[Any] = []

    fieldsets_fields_extend: List[Any] = ["service"]
    fieldsets_fields_remove: List[Any] = []

    autocomplete_fields = ("service", )
    list_select_related = (
        "service",
        "service__professional",
        "service__professional__user",
    )


@admin.register(ProfessionalClosedPeriod)
class ProfessionalClosedPeriodAdmin(
        ClosedPeriodMixin,
        ListFilterUpdateMixin,
        ListDisplayUpdateMixin,
        ListLinksUpdateMixin,
        FieldsetFieldsUpdateMixin,
):
    """The professional closed period admin class."""

    list_filter_extend: List[Any] = [ProfessionalFilter]
    list_filter_remove: List[Any] = []

    list_display_extend: List[Any] = ["professional"]
    list_display_remove: List[Any] = []

    list_links_extend: List[Any] = ["professional"]
    list_links_remove: List[Any] = []

    fieldsets_fields_extend: List[Any] = ["professional"]
    fieldsets_fields_remove: List[Any] = []

    autocomplete_fields = ("professional", )
    list_select_related = ("professional", "professional__user")


@admin.register(ServiceClosedPeriod)
class ServiceClosedPeriodAdmin(
        ClosedPeriodMixin,
        ListFilterUpdateMixin,
        ListDisplayUpdateMixin,
        ListLinksUpdateMixin,
        FieldsetFieldsUpdateMixin,
):
    """The service closed period admin class."""

    list_filter_extend: List[Any] = [ServiceFilter]
    list_filter_remove: List[Any] = []

    list_display_extend: List[Any] = ["service"]
    list_display_remove: List[Any] = []

    list_links_extend: List[Any] = ["service"]
    list_links_remove: List[Any] = []

    fieldsets_fields_extend: List[Any] = ["service"]
    fieldsets_fields_remove: List[Any] = []

    autocomplete_fields = ("service", )
    list_select_related = (
        "service",
        "service__professional",
        "service__professional__user",
    )


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(VersionAdmin):
    """The availability slot admin."""

    def weekday(self, obj: AvailabilitySlot) -> str:
        # pylint: disable=no-self-use
        """Return a weekday."""
        start = obj.start_datetime.strftime("%A")
        end = obj.end_datetime.strftime("%A")

        return start if start == end else f"{start} - {end}"

    def changelist_view(self, request, extra_context=None):
        """List the entries."""
        professional = Professional.objects.get_list().first()
        if not request.GET.get("professional__pk__exact") and professional:
            query = request.GET.copy()
            query["professional__pk__exact"] = professional.pk
            request.GET = query
            request.META["QUERY_STRING"] = request.GET.urlencode()
        return super().changelist_view(request, extra_context=extra_context)

    list_display = [
        "id", "start_datetime", "end_datetime", "weekday", "professional",
        "service"
    ]
    readonly_fields = ["weekday"]
    list_display_links = ["id"]
    list_filter = (
        "start_datetime",
        "end_datetime",
        ProfessionalFilter,
        ServiceFilter,
    )
    list_select_related = ("service", "professional", "professional__user")
    autocomplete_fields = ("service", "professional")

    class Media:
        """Required for the AutocompleteFilter."""
