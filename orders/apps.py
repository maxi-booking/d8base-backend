"""The orders apps module."""
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """The orders app configuration."""

    name = "orders"

    def ready(self) -> None:
        """Ready."""
        # pylint: disable=unused-import,import-outside-toplevel
        import orders.signals
