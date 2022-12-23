"""Module for OpenTable-specific handling of reservations.

Todo:
    * add querying of reservations for v0.5.0
    * add booking of reservations for v1.0.0

"""

from datetime import datetime as dt

from i_need_a_res.providers.models import ReservationProvider
from i_need_a_res.providers.models import ReservationSlot


def get_reservation(
    api_key: str, auth_token: str, city: str, search_day: dt, party_size: int
) -> ReservationSlot:
    """Stub function to return reservations."""
    return ReservationSlot(
        "Generic Restaurant",
        dt(2023, 4, 20, 6, 9, 0, 0),
        "token",
        ReservationProvider.OPENTABLE,
    )
