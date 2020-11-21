"""The orders tasks module."""
from communication.services import notify_reminders
from d8b.celery import app

from .models import OrderReminder


@app.task(soft_time_limit=60 * 30)
def notify_order_reminders():
    """Notify order reminders."""
    notify_reminders(OrderReminder)
