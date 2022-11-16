from typing import NamedTuple

from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim


USER_AGENT = str(__import__(__name__.split(".")[0]))


class GeoPoint(NamedTuple):
    latitude: float
    longitude: float


def convert_to_geopoint(latitude: str, longitude: str) -> GeoPoint:
    return GeoPoint(
        latitude=round(float(latitude), 6), longitude=round(float(longitude), 6)
    )


def get_city_geopoint(city: str) -> GeoPoint:
    with Nominatim(user_agent=USER_AGENT) as geolocator:
        location = geolocator.geocode(city)
    city_geopoint = GeoPoint(location.latitude, location.longitude)
    return city_geopoint
