"""Resy-specific models.

Todo:
* refactor venue and city models to inherit from common base model

"""
from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import List

from requests.auth import AuthBase
from requests.models import PreparedRequest

from i_need_a_res.geo_util.lib import GeoPoint
from i_need_a_res.lib import ReservationSlot


class ResyAuth(AuthBase):
    """Attaches Resy-required auth headers to the given Request or Session object.

    Attributes:
        api_key (str): Resy API key
        auth_token (str): Resy user JWT token

    """

    def __init__(self, api_key: str, auth_token: str) -> None:
        """Initializes the class.

        Args:
            api_key: Resy API key
            auth_token: Resy user JWT token

        """
        self.api_key = api_key
        self.auth_token = auth_token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        """Adds appropriate authorization headers to each request."""
        r.headers["Authorization"] = f'ResyAPI api_key="{self.api_key}"'
        r.headers["X-Resy-Auth-Token"] = self.auth_token
        return r


@dataclass
class ResyVenue:
    """Mutable data structure for Resy venues.

    Attributes:
        venue_id: Resy unique ID of the venue
        name: name of the venue
        cuisine: type of food the venue serves
        price_range: price range of the venue, from 1 to 4.
        rating: rating of the venue from Resy reviews
        coordinates: latitude and longitude of the venue.
        reservation_slots: a list of ReservationSlot objects representing the available slots.

    """

    venue_id: int
    name: str
    cuisine: str
    price_range: int
    rating: float
    coordinates: GeoPoint
    reservation_slots: List[ReservationSlot]


class ResyCities(Enum):
    """Data structure for the list of Resy-supported cities."""

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
