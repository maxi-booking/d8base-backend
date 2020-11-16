"""The settings init module."""
from .celery import *
from .custom import *
from .getter import get_settings
from .images import *
from .languages import *
from .main import *
from .messenger import *
from .orders import *
from .permissions import *
from .schedule import *
from .units import *

__all__ = ["get_settings"]
