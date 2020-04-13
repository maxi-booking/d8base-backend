"""The professionals admin module."""

from typing import Tuple, Type

from adminsortable.admin import SortableAdmin, SortableTabularInline
from django.contrib import admin
from modeltranslation.admin import (TabbedTranslationAdmin,
                                    TranslationTabularInline)
from reversion.admin import VersionAdmin

from .models import Category, Subcategory


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
