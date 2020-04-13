"""The professionals translation module."""

from modeltranslation.translator import TranslationOptions, register

from .models import Category, Subcategory


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """The category translation options class."""

    fields = ('name', 'description')
    required_languages = ('en', )


@register(Subcategory)
class SubcategoryTranslationOptions(CategoryTranslationOptions):
    """The subcategory translation options class."""
