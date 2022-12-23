"""Reservation providers."""
from random import choice
from typing import List

from i_need_a_res.providers.models import ReservationSlot
from i_need_a_res.providers.models import Venue


def _get_random_reservation(restaurant_list: List[Venue]) -> ReservationSlot:
    restaurant_choice = choice(restaurant_list)  # nosec B311
    while len(restaurant_choice.reservation_slots) == 0:
        restaurant_choice = choice(restaurant_list)  # nosec B311
    slot_choice = choice(restaurant_choice.reservation_slots)  # nosec B311
    return slot_choice
