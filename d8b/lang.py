"""The d8b lang module."""
from contextlib import contextmanager

from django.utils.translation import activate, get_language


@contextmanager
def select_locale(lang):
    """Set the locale."""
    try:
        old_lang = get_language()
        if lang != old_lang:
            activate(lang)
        yield None
    finally:
        if lang != old_lang:
            activate(old_lang)
