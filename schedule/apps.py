"""The schedule apps module."""
from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    """The schedule app configuration."""

    name: str = "schedule"

    def ready(self) -> None:
        """Ready."""
        # pylint: disable=unused-import,import-outside-toplevel
        import schedule.signals
