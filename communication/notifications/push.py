"""The notifications push module."""
from push_notifications.models import GCMDevice

from d8b.logging import log
from users.models import User

from .services import render_template, translate_subject


@log("An push message has been sent to the user.")
def send_push_message_user(
    user: User,
    subject: str,
    template: str,
    data: dict,
):
    """Send a push notification to a user."""
    lang = user.preferred_language

    GCMDevice.objects.filter(user=user).send_message(
        render_template(lang, template, "push", data),
        title=translate_subject(lang, subject),
    )
