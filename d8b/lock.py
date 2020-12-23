"""The distributed lock module."""

from functools import wraps
from typing import List, Optional

from redis.exceptions import RedisError

from d8b.redis import redis


def distributed_lock(
    prefix: Optional[str] = None,
    keys: Optional[List[str]] = None,
    timeout: Optional[int] = None,
):
    """Ensure only one instance gets invoked at a time."""

    def innter(func):
        """Run the inner functions."""

        @wraps(func)
        def with_lock(*args, **kwargs):
            """Run the function."""
            key = prefix if prefix else func.__name__
            if not keys:
                key += f"args_{args}_kwargs_{kwargs}"
            else:
                keys_values = {k: v for (k, v) in kwargs.items() if k in keys}
                if not keys_values:
                    raise ValueError("Keys are empty")
                key += f"keys_{keys_values}"
            func_result = None
            lock = redis.lock(key, timeout=timeout)
            try:
                lock.acquire(blocking=True)
                func_result = func(*args, **kwargs)
            finally:
                try:
                    lock.release()
                except RedisError:
                    pass
            return func_result

        return with_lock

    return innter
