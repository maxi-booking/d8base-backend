"""The orders admin module."""
from django.contrib import admin
from reversion.admin import VersionAdmin

from .admin_fiters import ClientFilter, ServiceFilter
from .models import Order


@admin.register(Order)
class OrderAdmin(VersionAdmin):
    """The order admin."""

    list_display = ("id", "service", "start_datetime", "end_datetime",
                    "status", "client", "created")
    readonly_fields = ("created", "modified", "created_by", "modified_by")
    list_display_links = ("id", )

    raw_id_fields = ("service_location", )
    autocomplete_fields = ("client", "service", "client_location")
    list_filter = (
        "start_datetime",
        "end_datetime",
        "status",
        ClientFilter,
        ServiceFilter,
    )

    search_fields = ("=id", "note", "first_name", "last_name", "phone",
                     "client__email", "service__name", "service__description")

    fieldsets = (
        ("General", {
            "fields": ("service", "status", "start_datetime", "end_datetime",
                       "note", "price", "service_location")
        }),
        ("Client", {
            "fields": ("client", "is_another_person", "first_name",
                       "last_name", "phone", "client_location")
        }),
        ("Options", {
            "fields": ("remind_before", "created", "modified", "created_by",
                       "modified_by")
        }),
    )
    list_select_related = (
        "service",
        "client",
        "service__professional",
        "service__professional__user",
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        """Return the admin form."""
        form = super().get_form(request, obj=None, change=False, **kwargs)
        form.base_fields["end_datetime"].required = False

        return form

    class Media:
        """Required for the AutocompleteFilter."""
