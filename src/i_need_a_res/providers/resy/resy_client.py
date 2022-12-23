"""Module for Resy API client.

Todo:
* add POST reservation routes for v1.0.0
* add rest of GET routes (eventually)
"""
from datetime import datetime as dt
from typing import Dict
from typing import List

from requests import Response
from requests.auth import AuthBase
from requests.models import PreparedRequest
from requests.sessions import Session

from i_need_a_res.geo import GeoPoint
from i_need_a_res.geo import convert_to_geopoint
from i_need_a_res.providers.models import ReservationProvider
from i_need_a_res.providers.models import ReservationSlot
from i_need_a_res.providers.models import Venue


RESY_API_URL = "https://api.resy.com"
"""str: Base URL for the Resy API"""


class ResyAuth(AuthBase):
    """Attaches Resy-required auth headers to the given Request or Session object.

    Attributes:
        api_key (str): Resy API key
        auth_token (str): Resy user JWT token

    """

    def __init__(self, api_key: str, auth_token: str) -> None:
        """Initializes the class.

        Args:
            api_key: Resy API key
            auth_token: Resy user JWT token

        """
        self.api_key = api_key  #: Resy API key
        self.auth_token = auth_token  #: Resy user JWT token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        """Adds appropriate authorization headers to each request."""
        r.headers["Authorization"] = f'ResyAPI api_key="{self.api_key}"'
        r.headers["X-Resy-Auth-Token"] = self.auth_token
        return r


class ResyClient:
    """Class for Resy API client.

    Attributes:
        sesssion (requests.sessions.Session): Session for requests to the Resy API
        session.auth (requests.sessions.Session.auth): Authorization information for the Resy API, persisting across requests.

    """

    __attrs__ = ["session"]

    def __init__(self, api_key: str, auth_token: str) -> None:
        """Initializes a session for API requests.

        Args:
            api_key: Resy API key
            auth_token: Resy user JWT token

        """
        self.session = Session()
        self.session.auth = ResyAuth(api_key=api_key, auth_token=auth_token)

    def _get(self, api_route: str, params: Dict[str, str] | None = None) -> Response:
        resp = self.session.get(
            url=f"{RESY_API_URL}/{api_route}",
            headers={
                "Content-Type": "x-www-form-urlencoded",
                "Accept": "application/json",
            },
            params=params,
        )
        return resp

    def _post(self, api_route: str, params: Dict[str, str] | None = None) -> Response:
        resp = self.session.post(
            url=f"{RESY_API_URL}/{api_route}", headers={"Accept": "application/json"}
        )
        return resp

    def get_venues(
        self, geolocation: GeoPoint, search_day: dt, party_size: int
    ) -> List[Venue]:
        """Method for returning all venues on Resy with available reservation slots for the given date, time, city, and party size.

        Args:
            geolocation: NamedTuple of the city's center coordinates
            search_day: Day to search reservations for.
            party_size: Size of party.

        Returns:
            A list of ResyVenue objects.

        """
        lat = geolocation.latitude
        long = geolocation.longitude
        day = search_day.strftime("%Y-%m-%d")

        resp = self._get(
            api_route="4/find",
            params={
                "lat": f"{lat}",
                "long": f"{long}",
                "day": day,
                "party_size": f"{party_size}",
            },
        )

        if not resp.ok:
            resp.raise_for_status()

        list_of_venues: List[Venue] = []
        for venue in resp.json()["results"]["venues"]:
            venue_id = venue["venue"]["id"]["resy"]
            venue_name = venue["venue"]["name"]
            venue_type = venue["venue"]["type"]
            venue_price_range = venue["venue"]["price_range"]
            venue_rating = venue["venue"]["rating"]
            venue_lat = str(venue["venue"]["location"]["geo"]["lat"])
            venue_lon = str(venue["venue"]["location"]["geo"]["lon"])
            venue_coordinates = convert_to_geopoint(
                latitude=venue_lat, longitude=venue_lon
            )
            venue_reservation_slots: List[ReservationSlot] = []
            for slot in venue["slots"]:
                slot_time = dt.strptime(slot["date"]["start"], "%Y-%m-%d %H:%M:%S")
                slot_token = slot["config"]["token"]
                venue_reservation_slots.append(
                    ReservationSlot(
                        restaurant_name=venue_name,
                        time=slot_time,
                        token=slot_token,
                        reservation_provider=ReservationProvider.RESY,
                    )
                )

            if len(venue_reservation_slots) > 0:
                list_of_venues.append(
                    Venue(
                        venue_id=venue_id,
                        name=venue_name,
                        cuisine=venue_type,
                        price_range=venue_price_range,
                        rating=venue_rating,
                        coordinates=venue_coordinates,
                        reservation_slots=venue_reservation_slots,
                    )
                )

        return list_of_venues
