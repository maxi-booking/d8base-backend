"""The notifications messenger module."""
from typing import List

from celery.app.task import Task
from django.utils.module_loading import import_string

from d8b.settings import get_settings
from users.models import User


class Messenger():
    """The messanger class."""

    # firebase
    messengers: List[Task] = []

    def __init__(self):
        """Construct the object."""
        for name in get_settings('D8B_MESSENGER_TASKS'):
            self.messengers.append(import_string(name))

    def send(
        self,
        user: User,
        subject: str,
        template: str,
        context: dict = None,
    ):
        """Send messages."""
        data = {
            'user_id': user.pk,
            'subject': subject,
            'template': template,
            'context': context,
        }
        for messanger in self.messengers:
            messanger.apply_async(kwargs=data)
