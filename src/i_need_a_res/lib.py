from datetime import datetime as dt
from enum import Enum
from typing import List
from typing import NamedTuple


class ReservationSlot(NamedTuple):
    restaurant_name: str
    time: dt
    token: str


class LocationError(ValueError):
    pass


def check_if_valid_city(candidate_city: str, city_list: Enum) -> bool:
    if candidate_city.lower() in [city.name.replace("_", " ").lower() for city in city_list]:  # type: ignore[attr-defined]
        return True
    else:
        return False


def return_prettified_valid_cities(city_list: Enum) -> List[str]:
    return [city.name.replace("_", " ").title() for city in city_list]  # type: ignore[attr-defined]
