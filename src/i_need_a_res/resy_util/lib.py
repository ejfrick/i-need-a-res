from dataclasses import dataclass
from typing import List

from requests.auth import AuthBase
from requests.models import PreparedRequest

from i_need_a_res.geo_util.lib import GeoPoint
from i_need_a_res.lib import Reservation


class ResyAuth(AuthBase):
    """Attaches Resy-required auth headers to the given Request or Session object."""

    def __init__(self, api_key: str, auth_token: str) -> None:
        self.api_key = api_key
        self.auth_token = auth_token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["Authorization"] = f"ResyAPI api_key='{self.api_key}'"
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
    reservation_slots: List[Reservation]
