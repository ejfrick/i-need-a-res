from datetime import datetime as dt

from i_need_a_res.lib import ReservationSlot


def get_reservation(
    api_key: str, auth_token: str, city: str, search_day: dt, party_size: int
) -> ReservationSlot:
    return ReservationSlot("Generic Restaurant", dt(2023, 4, 20, 6, 9, 0, 0), "token")
