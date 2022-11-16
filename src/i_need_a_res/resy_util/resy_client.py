import requests
import logging
from requests.sessions import Session
from requests import Response
from typing import TypeVar, List, Dict
from datetime import datetime as dt
from i_need_a_res.resy_util.lib import ResyAuth, ResyVenue
from i_need_a_res.geo_util.lib import GeoPoint, convert_to_geopoint
from i_need_a_res.lib import Reservation

TResyClient = TypeVar("TResyClient")
RESY_API_URL = "https://api.resy.com"

class ResyClient():    
    __attrs__ = ["session"]

    def __init__(self, api_key: str, auth_token: str) -> None:
        self.session = Session()
        self.session.auth = ResyAuth(api_key=api_key, auth_token=auth_token)

    def _get(self, api_route: str, params: Dict[str, str] | None = None) -> Response:
        resp = self.session.get(url=f"{RESY_API_URL}/{api_route}", headers={"Content-Type": "x-www-form-urlencoded", "Accept": "application/json"}, params=params)
        return resp
    
    def _post(self, api_route: str, params: Dict[str, str] | None = None) -> Response:
        resp = self.session.post(url=f"{RESY_API_URL}/{api_route}", headers={"Accept": "application/json"})
        return resp

    def get_venues(self, geolocation: GeoPoint, search_day: dt, party_size: int) -> List[ResyVenue]:
        lat = geolocation.latitude
        long = geolocation.longitude
        day = search_day.strftime("%Y-%m-%d")

        resp = self._get(api_route="4/find", params={"lat": f"{lat}", "long": f"{long}", "day": day, "party_size": f"{party_size}"})

        if not resp.ok:
            resp.raise_for_status()
        
        list_of_venues: List[ResyVenue] = []
        for venue in resp.json()["results"]["venues"]:
            venue_id = venue["venue"]["id"]["resy"]
            venue_name = venue["venue"]["name"]
            venue_type = venue["venue"]["type"]
            venue_price_range = venue["venue"]["price_range"]
            venue_rating = venue["venue"]["rating"]
            venue_lat = str(venue["venue"]["location"]["geo"]["lat"])
            venue_lon = str(venue["venue"]["location"]["geo"]["lon"])
            venue_coordinates = convert_to_geopoint(latitude=venue_lat, longitude=venue_lon)
            venue_reservation_slots: List[Reservation] = []
            for slot in venue["slots"]:
                slot_time = dt.strptime(slot["date"]["start"], "%Y-%m-%d %H:%M:%S")
                slot_token = slot["config"]["token"]
                venue_reservation_slots.append(Reservation(time=slot_time, token=slot_token))

            list_of_venues.append(ResyVenue(venue_id=venue_id, name=venue_name, cuisine=venue_type, price_range=venue_price_range, rating=venue_rating, coordinates=venue_coordinates, reservation_slots=venue_reservation_slots))
        
        return list_of_venues
