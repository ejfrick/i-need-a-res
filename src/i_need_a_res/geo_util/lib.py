from typing import NamedTuple


class GeoPoint(NamedTuple):
    latitude: float
    longitude: float


def convert_to_geopoint(latitude: str, longitude: str) -> GeoPoint:
    return GeoPoint(latitude=round(float(latitude), 6), longitude=round(float(longitude), 6))
