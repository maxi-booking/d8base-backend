"""The fields tests module."""
from django.conf import settings

from d8b.fields import LanguageField


def test_language_field():
    """Should create a language field."""
    field = LanguageField()
    assert field.max_length == 2
    assert field.choices == settings.LANGUAGES
