"""The environment module."""
import os

import environ

ROOT = environ.Path(__file__) - 3


def get_env() -> environ.Env:
    """Return the ENV."""
    env = environ.Env()

    run_env = env.str('RUN_ENV', default='')

    env_file = '.env_' + run_env if run_env else '.env'
    environ.Env.read_env(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            env_file,
        ))
    return env
