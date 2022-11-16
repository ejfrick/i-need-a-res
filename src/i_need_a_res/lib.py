from datetime import datetime as dt
from datetime import timedelta as td
from enum import Enum
from typing import List
from typing import NamedTuple


class ReservationSlot(NamedTuple):
    restaurant_name: str
    time: dt
    token: str

    def __str__(self) -> str:
        """Returns ReservationSlot in human-friendly format."""
        hour_min = self.time.strftime("%H:%M")
        return f"a reservation at {self.restaurant_name} at {hour_min} on {self.time.month}/{self.time.day}"


class LocationError(ValueError):
    pass


def check_if_valid_city(candidate_city: str, city_list: Enum) -> bool:
    if candidate_city.lower() in [city.name.replace("_", " ").lower() for city in city_list]:  # type: ignore[attr-defined]
        return True
    else:
        return False


def return_prettified_valid_cities(city_list: Enum) -> List[str]:
    return [city.name.replace("_", " ").title() for city in city_list]  # type: ignore[attr-defined]


def convert_book_date_to_datetime(book_date: str) -> dt:
    if book_date.lower() == "today":
        book_datetime = dt.now()
    elif book_date.lower() == "tomorrow":
        book_datetime = dt.now() + td(days=1)
    else:
        book_datetime = dt.strptime(book_date, "%m/%d/%Y")

    return book_datetime
