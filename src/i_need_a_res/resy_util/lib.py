from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import List

from requests.auth import AuthBase
from requests.models import PreparedRequest

from i_need_a_res.geo_util.lib import GeoPoint
from i_need_a_res.lib import ReservationSlot


class ResyAuth(AuthBase):
    """Attaches Resy-required auth headers to the given Request or Session object."""

    def __init__(self, api_key: str, auth_token: str) -> None:
        self.api_key = api_key
        self.auth_token = auth_token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["Authorization"] = f'ResyAPI api_key="{self.api_key}"'
        r.headers["X-Resy-Auth-Token"] = self.auth_token
        return r


@dataclass
class ResyVenue:
    venue_id: int
    name: str
    cuisine: str
    price_range: int
    rating: float
    coordinates: GeoPoint
    reservation_slots: List[ReservationSlot]


class ResyCities(Enum):
    ATLANTA = auto()
    AUSTIN = auto()
    BERLIN = auto()
    BOSTON = auto()
    CHARLESTON = auto()
    CHICAGO = auto()
    DALLAS = auto()
    FORT_WORTH = auto()
    DENVER = auto()
    DETROIT = auto()
    HAMPTONS = auto()
    HOUSTON = auto()
    LONDON = auto()
    LOS_ANGELES = auto()
    MIAMI = auto()
    MINNEAPOLIS = auto()
    NAPA = auto()
    NASHVILLE = auto()
    NEW_ORLEANS = auto()
    NEW_YORK = auto()
    PHILADELPHIA = auto()
    PORTLAND = auto()
    SAN_FRANCISCO = auto()
    SEATTLE = auto()
    SYDNEY = auto()
    TORONTO = auto()
    WASHINGTON_DC = auto()
