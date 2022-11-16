from typing import NamedTuple
from datetime import datetime as dt


class Reservation(NamedTuple):
    time: dt
    token: str
