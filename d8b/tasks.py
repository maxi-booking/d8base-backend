"""The d8b tasks module."""
from django.utils.module_loading import import_string
from djmoney import settings

from .celery import app


@app.task
def update_rates(backend=settings.EXCHANGE_BACKEND, **kwargs):
    """Update the currency rates."""
    backend = import_string(backend)()
    backend.update_rates(**kwargs)
