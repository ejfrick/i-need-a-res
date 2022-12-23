"""Module for Resy-specific handling of reservations.

Todo:
    * add booking of reservations for v1.0.0

"""

from datetime import datetime as dt
from datetime import timedelta as td

from i_need_a_res import LocationError
from i_need_a_res.geo import get_city_geopoint
from i_need_a_res.providers import _get_random_reservation
from i_need_a_res.providers.models import ReservationSlot
from i_need_a_res.providers.models import ResyCities
from i_need_a_res.providers.resy.resy_client import ResyClient


def _get_client(api_key: str, auth_token: str) -> ResyClient:
    client = ResyClient(api_key=api_key, auth_token=auth_token)
    return client


def get_reservation(
    api_key: str, auth_token: str, city: str, search_day: dt, party_size: int
) -> ReservationSlot:
    """Function to orchestrate getting a random reservation.

    Args:
        api_key: Resy API key
        auth_token: Resy user JWT token
        city: city to search for reservations in
        search_day: day to search reservations for
        party_size: size of the party

    Returns:
        A ReservationSlot object

        Example:
            >>> ReservationSlot("The French Laundry", datetime(2023, 01, 01, 19, 00), "some_token_value")

    Raises:
        LocationError: if city is not a supported Resy city.

    """
    if city not in ResyCities:
        raise LocationError(
            f"City {city} is not a valid city. Valid cities are {ResyCities}"
        )

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
