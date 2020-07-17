"""The communication translation module."""

from modeltranslation.translator import TranslationOptions, register

from .models import SuggestedMessage


@register(SuggestedMessage)
class SuggestedMessageTranslationOptions(TranslationOptions):
    """The suggested answer translation options class."""

    fields = ("name", "body")
    required_languages = ("en", )
