"""The d8b admin module."""
from typing import Any, List

import adminactions.actions as actions
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import site
from django.http.request import HttpRequest
from django_otp.admin import OTPAdminSite

if not settings.TESTS:
    admin.site.__class__ = OTPAdminSite

actions.add_to_site(site)
admin.site.site_header = admin.site.site_title = 'D8B admin'
admin.site.site_url = '/api/'


class SearchFieldsUpdateMixin(admin.ModelAdmin):
    """The mixin to update the search fields."""

    search_fields_extend: List[Any] = []
    search_fields_remove: List[Any] = []

    def get_search_fields(self, request: HttpRequest) -> List[Any]:
        """Admin search fields."""
        search_fields = list(super().get_search_fields(request))
        search_fields.extend(self.search_fields_extend)
        return [f for f in search_fields if f not in self.search_fields_remove]


class ListFilterUpdateMixin(admin.ModelAdmin):
    """The mixin to update the list filters fields."""

    list_filter_extend: List[Any] = []
    list_filter_remove: List[Any] = []

    def get_list_filter(self, request: HttpRequest) -> List[Any]:
        """Admin list filter."""
        list_filter = list(super().get_list_filter(request))
        list_filter.extend(self.list_filter_extend)
        return [f for f in list_filter if f not in self.list_filter_remove]


class ListDisplayUpdateMixin(admin.ModelAdmin):
    """The mixin to update the list display fields."""

    list_display_extend: List[Any] = []
    list_display_remove: List[Any] = []

    def get_list_display(self, request):
        """Admin list filter."""
        list_display = list(super().get_list_display(request))
        list_display.extend(self.list_display_extend)
        return [f for f in list_display if f not in self.list_display_remove]
