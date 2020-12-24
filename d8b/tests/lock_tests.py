"""The lock tests module."""
import threading
from time import sleep

import pytest

from d8b.lock import distributed_lock
from d8b.redis import redis

LOCK_NAME: str = "test_args_()_kwargs_{}"
PREFIX: str = "test"


def _run_functions(one, two):
    """Run the functions."""
    thread1 = threading.Thread(target=one)
    thread2 = threading.Thread(target=two)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


def _check_parallel_run(key: str):
    """Run in parallel."""
    redis.delete(key)

    def test1():
        """The test function."""
        sleep(1)
        redis.set(key, "slow")

    def test2():
        """The test function."""
        redis.set(key, "quick")

    _run_functions(test1, test2)
    assert redis.get(key) == b"slow"


def _check_sequential_run(key: str):
    """Run sequentially."""
    redis.delete(LOCK_NAME)
    redis.delete(key)

    @distributed_lock(prefix=PREFIX)
    def test1():
        """The test function."""
        sleep(1)
        redis.set(key, "slow")

    @distributed_lock(prefix=PREFIX)
    def test2():
        """The test function."""
        redis.set(key, "quick")

    _run_functions(test1, test2)

    assert redis.get(key) == b"quick"


def test_distributed_lock():
    """Should create a lock."""
    key = "test_key"
    _check_parallel_run(key)
    _check_sequential_run(key)


def test_distributed_lock_exceptions():
    """Should throw exceptions."""
    redis.delete(LOCK_NAME)

    @distributed_lock(prefix=PREFIX, keys=["invalid"])
    def test():
        """The test function."""

    with pytest.raises(ValueError) as error:
        test()

    assert "Keys are empty" in str(error)


def test_distributed_lock_expired_lock():
    """Should be able to run."""
    redis.delete(LOCK_NAME)

    @distributed_lock(prefix=PREFIX, timeout=0.5)
    def test():
        """The test function."""
        sleep(1)

    test()
