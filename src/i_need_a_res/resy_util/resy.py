from datetime import datetime as dt
from datetime import timedelta as td
from random import choice
from typing import List

from i_need_a_res.geo_util.lib import GeoPoint
from i_need_a_res.geo_util.lib import get_city_geopoint
from i_need_a_res.lib import LocationError
from i_need_a_res.lib import ReservationSlot
from i_need_a_res.lib import check_if_valid_city
from i_need_a_res.lib import return_prettified_valid_cities
from i_need_a_res.resy_util.lib import ResyCities
from i_need_a_res.resy_util.lib import ResyVenue
from i_need_a_res.resy_util.resy_client import ResyClient


def _get_client(api_key: str, auth_token: str) -> ResyClient:
    client = ResyClient(api_key=api_key, auth_token=auth_token)
    return client


def _get_random_reservation(restaurant_list: List[ResyVenue]) -> ReservationSlot:
    restaurant_choice = choice(restaurant_list)  # nosec B311
    while len(restaurant_choice.reservation_slots) == 0:
        restaurant_choice = choice(restaurant_list)
    slot_choice = choice(restaurant_choice.reservation_slots)  # nosec B311
    return slot_choice


def get_reservation(
    api_key: str, auth_token: str, city: str, search_day: dt, party_size: int
) -> ReservationSlot:
    if not check_if_valid_city(candidate_city=city, city_list=ResyCities):  # type: ignore[arg-type]
        raise LocationError(f"City {city} is not a valid city. Valid cities are {return_prettified_valid_cities(ResyCities)}")  # type: ignore[arg-type]

    city_geopoint = get_city_geopoint(city)

    resy_client = _get_client(api_key=api_key, auth_token=auth_token)

    candidates = resy_client.get_venues(
        geolocation=city_geopoint, search_day=search_day, party_size=party_size
    )

    if len(candidates) == 0:
        candidates = resy_client.get_venues(
            geolocation=city_geopoint,
            search_day=search_day + td(days=1),
            party_size=party_size,
        )

    reservation = _get_random_reservation(candidates)

    return reservation
