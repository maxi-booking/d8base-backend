"""The professionals admin module."""

from typing import Tuple, Type

from adminsortable.admin import SortableAdmin, SortableTabularInline
from django.contrib import admin
from modeltranslation.admin import (TabbedTranslationAdmin,
                                    TranslationTabularInline)
from reversion.admin import VersionAdmin

from users.admin_fiters import UserFilter

from .models import Category, Professional, ProfessionalTag, Subcategory


class SubcategoryInlineAdmin(SortableTabularInline, TranslationTabularInline):
    """The subcategories admin class."""

    model = Subcategory
    fields = ('id', 'name', 'description', 'created', 'modified', 'created_by',
              'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    extra = 3


@admin.register(Category)
class CategoryAdmin(SortableAdmin, VersionAdmin, TabbedTranslationAdmin):
    """The categories admin class."""

    model: Type = Category
    list_display = ('id', 'name', 'created', 'created_by')
    search_fields = ('=id', 'name')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    change_list_template_extends = 'reversion/change_list.html'

    inlines = (SubcategoryInlineAdmin, )

    fieldsets: Tuple = (
        ('General', {
            'fields': ('name', 'description')
        }),
        ('Options', {
            'fields': ('created', 'modified', 'created_by', 'modified_by')
        }),
    )
    list_select_related = ('created_by', )


class ProfessionalTagInlineAdmin(admin.TabularInline):
    """The subcategories admin class."""

    model = ProfessionalTag
    fields = ('id', 'name', 'created', 'modified', 'created_by', 'modified_by')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    classes = ['collapse']
    extra = 3


@admin.register(Professional)
class ProfessionalAdmin(VersionAdmin):
    """The professional admin class."""

    model: Type = Professional
    list_display = ('id', 'name', 'subcategory', 'level', 'experience', 'user',
                    'created_by')
    list_display_links = ('id', 'name')
    search_fields = ('=id', 'name', 'user__email', 'user__lastname')
    readonly_fields = ('created', 'modified', 'created_by', 'modified_by')
    list_filter = ('level', 'subcategory', UserFilter)
    autocomplete_fields = ('user', )
    inlines = (ProfessionalTagInlineAdmin, )

    fieldsets: Tuple = (
        ('General', {
            'fields': ('name', 'description', 'company', 'subcategory')
        }),
        ('Experience', {
            'fields': ('experience', 'level')
        }),
        ('Options', {
            'fields': ('is_auto_order_confirmation', 'user', 'created',
                       'modified', 'created_by', 'modified_by')
        }),
    )
    list_select_related = ('created_by', 'subcategory', 'user')

    class Media:
        """Required for the AutocompleteFilter."""
