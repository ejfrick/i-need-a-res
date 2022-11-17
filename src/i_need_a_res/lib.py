"""Various helper functions and classes used by the provider modules and CLI."""

from datetime import datetime as dt
from datetime import timedelta as td
from enum import Enum
from enum import auto
from typing import List
from typing import NamedTuple


class ReservationProvider(Enum):
    """Data class to store available reservation providers."""

    RESY = auto()
    OPENTABLE = auto()


class ReservationSlot(NamedTuple):
    """Immutable data structure for reservation slots.

    Attributes:
        restaurant_name:
        time: datetime object of the reservation
        token: the reservation provider token for the particular reservation slot
        reservation_provider: Resy or OpenTable

    """

    restaurant_name: str
    time: dt
    token: str
    reservation_provider: ReservationProvider

    def __str__(self) -> str:
        """Returns the ReservationSlot in a human-friendly format.

        Example:
            >>> print(str(ReservationSlot("The French Laundry", datetime(2023, 01, 01, 19, 00), "some_token_value"))
                "a reservation at The French Laundry at 19:00 on 01/01"

        """
        hour_min = self.time.strftime("%H:%M")
        provider = str(ReservationProvider.name)
        return f"a reservation at {self.restaurant_name} at {hour_min} on {self.time.month}/{self.time.day} from {provider.title()}"


class LocationError(ValueError):
    """A custom exception for invalid locations."""

    pass


def check_if_valid_city(candidate_city: str, city_list: Enum) -> bool:
    """Validator to check if a city is in an Enum.

    Notes:
        Can also be used to validate if any str is in an Enum with auto() values.

    Args:
        candidate_city:
        city_list: an Enum with string literal member names.

    Returns:
        True if candidate_city is in Enum, False otherwise.

    """
    if candidate_city.lower() in [city.name.replace("_", " ").lower() for city in city_list]:  # type: ignore[attr-defined]
        return True
    else:
        return False


def return_prettified_valid_cities(city_list: Enum) -> List[str]:
    """Returns the member names of a Enum as a list of title case strings.

    Args:
        city_list: an Enum with string literal member names.

    Returns:
        List of title-case string Enum member names.

    Todo:
        Eliminate this function by creating a Enum class that provider-level city lists inherit from that has a similar method.

    """
    return [city.name.replace("_", " ").title() for city in city_list]  # type: ignore[attr-defined]


def convert_book_date_to_datetime(book_date: str) -> dt:
    """Converts human-friendly date options into a datetime object.

    Args:
        book_date: date to book reservation

    Returns:
        A datetime object representation of the book date.

    """
    if book_date.lower() == "today":
        book_datetime = dt.now()
    elif book_date.lower() == "tomorrow":
        book_datetime = dt.now() + td(days=1)
    else:
        book_datetime = dt.strptime(book_date, "%m/%d/%Y")

    return book_datetime
