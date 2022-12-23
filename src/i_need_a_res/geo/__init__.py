"""Utils for geolocations."""
from typing import NamedTuple

from geopy.geocoders import Nominatim


USER_AGENT = str(__import__(__name__.split(".")[0]))
"""str: app name for querying the Nominatim API."""


class GeoPoint(NamedTuple):
    """Dataclass for geolocations.

    Parameters:
        latitude: latitude of location
        longitude: longitude of location

    """

    latitude: float  #: latitude of location
    longitude: float  #: longitude of location


def convert_to_geopoint(latitude: str, longitude: str) -> GeoPoint:
    """Helper function to convert string lat & long to a GeoPoint.

    Args:
        latitude: string latitude
        longitude: string longitude

    Returns:
        GeoPoint from strings.

    """
    return GeoPoint(
        latitude=round(float(latitude), 6), longitude=round(float(longitude), 6)
    )


def get_city_geopoint(city: str) -> GeoPoint:
    """Function to get the latitude and longitude from a str representing a city.

    Args:
        city: name of the city

    Returns:
        GeoPoint of the city center

    """
    with Nominatim(user_agent=USER_AGENT) as geolocator:
        location = geolocator.geocode(city)
    city_geopoint = GeoPoint(location.latitude, location.longitude)
    return city_geopoint
