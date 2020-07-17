"""The notifications email module."""
from django.core.mail import mail_managers as base_mail_managers
from django.core.mail import send_mail
from django.template.loader import render_to_string

from d8b.logging import log
from d8b.settings import get_settings
from users.models import User

from .services import render_template, translate_subject


@log("An email has been sent to the manangers")
def mail_managers(
    subject,
    data: dict,
    template: str = "emails/base_manager.html",
):
    """Send an email to manangers."""
    base_mail_managers(subject=subject,
                       message="",
                       html_message=render_to_string(template, data))


@log("An mail has been sent to the user.")
def mail_user(user: User, subject: str, template: str, data: dict):
    """Send an email to the user."""
    lang = user.preferred_language
    subject_text = get_settings("EMAIL_SUBJECT_PREFIX")
    subject_text += translate_subject(lang, subject)

    send_mail(
        recipient_list=[user.email],
        from_email=get_settings("DEFAULT_FROM_EMAIL"),
        subject=subject_text,
        message="",
        html_message=render_template(lang, template, "emails", data),
    )
