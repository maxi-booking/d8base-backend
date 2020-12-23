"""The redis module."""
from django.conf import settings
from redis import Redis

redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)
