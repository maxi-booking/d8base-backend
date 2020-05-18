"""The logging utilities."""
import logging
from functools import wraps


def log(message: str):
    """Decorate the function for logging result."""

    def innter(func):
        """Run the inner func."""

        @wraps(func)
        def with_log(*args, **kwargs):
            """Run the func."""
            result = func(*args, **kwargs)

            logging.getLogger('d8b').info(
                '%s; args: %s; kwargs: %s',
                message,
                args,
                kwargs,
            )
            return result

        return with_log

    return innter
