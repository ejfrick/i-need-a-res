"""Module for OpenTable-specific handling of reservations.

Todo:
    * add querying of reservations for v0.5.0
    * add booking of reservations for v1.0.0

"""

from datetime import datetime as dt

from i_need_a_res.geo_util.lib import get_city_geopoint
from i_need_a_res.lib import LocationError
from i_need_a_res.lib import ReservationProvider
from i_need_a_res.lib import ReservationSlot
from i_need_a_res.lib import check_if_valid_city
from i_need_a_res.lib import return_prettified_valid_cities
from i_need_a_res.opentable_util.lib import OpenTableCities
from i_need_a_res.opentable_util.opentable_client import OpenTableClient


def _get_client(api_key: str, auth_token: str) -> OpenTableClient:
    client = OpenTableClient(api_key=api_key, auth_token=auth_token)
    return client


def get_reservation(
    api_key: str, auth_token: str, city: str, search_day: dt, party_size: int
) -> ReservationSlot:
    """Stub function to return reservations."""

    if not check_if_valid_city(candidate_city=city, city_list=OpenTableCities):  # type: ignore[arg-type]
        raise LocationError(f"City {city} is not a valid city. Valid cities are {return_prettified_valid_cities(OpenTableCities)}")  # type: ignore[arg-type]

    city_geopoint = get_city_geopoint(city=city)

    opentable_client = _get_client(api_key=api_key, auth_token=auth_token)

    return ReservationSlot(
        "Generic Restaurant",
        dt(2023, 4, 20, 6, 9, 0, 0),
        "token",
        ReservationProvider.OPENTABLE,
    )
