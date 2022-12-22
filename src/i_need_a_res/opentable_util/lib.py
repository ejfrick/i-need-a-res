"""OpenTable-specific models.

Todo:
* refactor venue and city models to inherit from common base model

"""
from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import List

from requests.auth import AuthBase
from requests.models import PreparedRequest

from i_need_a_res.lib import ReservationSlot


class OpenTableCities(Enum):
    """Datastructure for OpenTable supported cities."""

    PORTLAND = auto()


@dataclass
class OpenTableVenue:
    """Mutuable data structur for OpenTable venues.

    Attributes:
        reservation_slots: a list of ReservationSlot objects

    """

    reservation_slots: List[ReservationSlot]


class OpenTableAuth(AuthBase):
    def __init__(self, api_key: str, auth_token: str) -> None:
        self.api_key = api_key
        self.auth_token = auth_token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["Authorization"] = f'OpenTableAPI api_key="{self.api_key}"'
        r.headers["X-OpenTable-Auth-Token"] = self.auth_token
        return r
