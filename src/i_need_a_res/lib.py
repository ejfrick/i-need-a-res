from datetime import datetime as dt
from typing import NamedTuple


class Reservation(NamedTuple):
    time: dt
    token: str
