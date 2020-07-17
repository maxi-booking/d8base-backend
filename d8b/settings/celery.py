"""The celery settings module."""
from .main import ENV

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
    }
}
CELERY_IMPORTS = ("communication.notifications.tasks", )
