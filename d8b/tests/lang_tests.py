"""The lang tests module."""
from django.utils.translation import get_language

from d8b.lang import select_locale


def test_set_locale():
    """Should set a temporary language."""
    assert get_language() == 'en'
    with select_locale('de'):
        assert get_language() == 'de'
    assert get_language() == 'en'
