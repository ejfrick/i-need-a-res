"""Data models for provider-related classes."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from enum import auto
from typing import List
from typing import NamedTuple

from i_need_a_res.geo import GeoPoint


ResyCities = frozenset(
    {
        "Atlanta",
        "Austin",
        "Berlin",
        "Boston",
        "Charleston",
        "Chicago",
        "Dallas",
        "Fort Worth",
        "Denver",
        "Detroit",
        "The Hamptons",
        "Houston",
        "Los Angeles",
        "Miami",
        "Minneapolis",
        "Napa",
        "Nashville",
        "New Orleans",
        "New York",
        "Philadelphia",
        "Portland",
        "San Francisco",
        "Seattle",
        "Sydney",
        "Toronto",
        "Washington, D.C.",
    }
)
OpenTableCities = frozenset({"Portland"})


class ReservationProvider(Enum):
    """Data class to store available reservation providers.

    Currently, only Resy and OpenTable are supported.

    """

    RESY = auto()
    OPENTABLE = auto()


class ReservationSlot(NamedTuple):
    """Immutable data structure for reservation slots.

    Parameters:
        restaurant_name: Name of the restaurant
        time: Time of reservation
        token: Reservation provider token
        reservation_provider: Name of provider

    """

    restaurant_name: str  #: Name of the restaurant
    time: datetime  #: Time of reservation
    token: str  #: Reservation provider token
    reservation_provider: ReservationProvider  #: Name of provider

    def __str__(self) -> str:
        """Returns the ReservationSlot in a human-friendly format.

        Example:
            >>> print(str(ReservationSlot("The French Laundry", datetime(2023, 01, 01, 19, 00), "some_token_value"))
                "a reservation at The French Laundry at 19:00 on 01/01"

        """
        hour_min = self.time.strftime("%H:%M")
        provider = str(self.reservation_provider.name)
        return f"a reservation at {self.restaurant_name} at {hour_min} on {self.time.month}/{self.time.day} from {provider.title()}"


@dataclass
class Venue:
    """Mutable data structure for venues.

    Attributes:
        venue_id: unique ID of the venue
        name: name of the venue
        cuisine: type of food the venue serves
        price_range: price range of the venue, from 1 to 4.
        rating: rating of the venue from reviews
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
