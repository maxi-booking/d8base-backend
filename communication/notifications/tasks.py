"""The communication tasks module."""
from d8b.celery import app
from users.models import User

from .email import mail_user


@app.task
def send_email(user_id: int, subject: str, template: str, context: dict):
    """Send a email to the user."""
    mail_user(
        user=User.objects.get(pk=user_id),
        subject=subject,
        template=template,
        data=context,
    )
