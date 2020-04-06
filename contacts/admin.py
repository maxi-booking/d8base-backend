"""The contacts admin module."""
from typing import Tuple, Type

from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(VersionAdmin):
    """The contacts admin class."""

    model: Type = Contact
    list_display = ('id', 'name', 'created', 'created_by')
    list_filter = ('countries', 'excluded_countries')
    search_fields = ('=id', 'name')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')

    autocomplete_fields = ('countries', 'excluded_countries')

    fieldsets: Tuple = (
        ('General', {
            'fields': ('name', 'countries', 'excluded_countries')
        }),
        ('Options', {
            'fields': ('created', 'modified', 'created_by', 'modified_by')
        }),
    )
    list_select_related = ('created_by', )
