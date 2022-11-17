"""OpenTable-specific models.

Todo:
* refactor venue and city models to inherit from common base model

"""
from enum import Enum
from enum import auto


class OpenTableCities(Enum):
    """Datastructure for OpenTable supported cities."""

    PORTLAND = auto()
