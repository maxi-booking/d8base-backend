"""The notifications push module."""
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from d8b.lang import select_locale


def translate_subject(lang: str, subject: str) -> str:
    """Translate the subject."""
    with select_locale(lang):
        subject = str(_(subject))
        return subject


def render_template(
    lang: str,
    template: str,
    folder: str,
    data: dict,
) -> str:
    """Render the template."""
    with select_locale(lang):
        template_path = f"{folder}/{template}.html"
        message = render_to_string(template_path, data)
        return message
