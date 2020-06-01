"""The communication app module."""
from django.apps import AppConfig


class CommunicationConfig(AppConfig):
    """The communication app configuration."""

    name: str = 'communication'

    def ready(self):
        """Ready."""
        # pylint: disable=all
        import communication.signals
