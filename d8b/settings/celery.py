"""The celery settings module."""
from celery.schedules import crontab
from kombu import Queue

from .main import ENV

# Celery
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_APP = "d8b"
CELERY_QUEUES = (
    Queue("default"),
    Queue("priority_high"),
)
CELERY_DEFAULT_QUEUE = "default"
CELERYD_TASK_SOFT_TIME_LIMIT = 60 * 5

CELERY_LOGLEVEL = ENV.str("CELERY_LOGLEVEL")
BROKER_URL = ENV.str("BROKER_URL")
CELERY_RESULT_BACKEND = ENV.str("CELERY_RESULT_BACKEND")
CELERY_ALWAYS_EAGER = ENV.bool("CELERY_ALWAYS_EAGER", default=False)
CELERY_EAGER_PROPAGATES_EXCEPTIONS = ENV.bool(
    "CELERY_EAGER_PROPAGATES_EXCEPTIONS", default=False)
if ENV.str("BROKER_BACKEND", default=None):
    BROKER_BACKEND = ENV.str("BROKER_BACKEND")

CELERYBEAT_SCHEDULE = {
    "update_rates": {
        "task": "d8b.tasks.update_rates",
        "schedule": 60 * 60 * 24
    },
    "notify_order_reminders": {
        "task": "orders.tasks.notify_order_reminders",
        "schedule": 60 * 5
    },
    "remove_expired_availability_slots_task": {
        "task": "schedule.tasks.remove_expired_availability_slots",
        "schedule": crontab(minute="0", hour="1", day_of_week="*")
    },
    "generate_future_availability_slots": {
        "task": "schedule.tasks.generate_future_availability_slots_task",
        "schedule": crontab(minute="0", hour="2", day_of_week="*")
    }
}
CELERY_IMPORTS = (
    "communication.notifications.tasks",
    "schedule.availability.tasks",
)
