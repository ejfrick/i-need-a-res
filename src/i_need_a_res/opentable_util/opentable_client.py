import ast
import json
import re
from datetime import datetime as dt
from pprint import pprint
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from bs4 import BeautifulSoup
from requests import Response
from requests.sessions import Session

from i_need_a_res.geo_util.lib import GeoPoint
from i_need_a_res.opentable_util.lib import OpenTableAuth
from i_need_a_res.opentable_util.lib import OpenTableVenue


OPENTABLE_API_URL = "https://mobile-api.opentable.com/api"


class OpenTableClient:

    __attrs__ = ["session"]

    def __init__(self, api_key: str, auth_token: str) -> None:
        self.session = Session()
        self.session.auth = OpenTableAuth(api_key=api_key, auth_token=auth_token)

    def _get_api(
        self, api_route: str, params: Optional[Dict[str, Any]] = None
    ) -> Response:
        resp = self.session.get(
            url=f"{OPENTABLE_API_URL}/{api_route}",
            headers={"Accept": "application/json"},
            params=params,
        )

        return resp

    def _get(self, route: str, params: Optional[Dict[str, Any]] = None) -> Response:
        resp = self.session.get(
            url=f"https://www.opentable.com/{route}",
            params=params,
            headers={"User-Agent": "I Need A Res"},
        )

        return resp

    def _santize_json(self, ugly_json: str) -> Dict[str, Any]:
        ugly_json = ugly_json.replace("\\", "").replace("\\", "").replace("\n", " ")

        reg = re.compile(
            '("description"\\:"[a-zA-Z\\s\\d\\-\\.\\,\'!\\?\\-]*)"([a-zA-Z\\s\\d\\-\\.\\,\'\\?\\-!]*(?<!"\\,))"(.*"\\,"topReview".*)'
        )

        reg_again = re.compile(
            '("highlightedText"\\:")[a-zA-Z\\s\\d\\-\\.\\,\'"\\-!\\?]*(?<!"\\,)("\\,"\\_\\_typename")',
            re.MULTILINE,
        )

        medium_rare_json = re.sub(reg, r"\g<1> \g<2> \g<3>", ugly_json)

        medium_json = re.sub(reg_again, r"\g<1> \g<2>", medium_rare_json)

        medium_well_json = re.sub(reg, r"\g<1> \g<2> \g<3>", medium_json)

        sanitized_json: Dict[str, Any] = json.loads(medium_well_json)

        return sanitized_json

    def get_venues(
        self, geolocation: GeoPoint, search_day: dt, party_size: int
    ) -> List[OpenTableVenue]:
        lat = geolocation.latitude
        long = geolocation.longitude
        day = search_day.strftime("%Y-%m-%dT%H:%M:%S")

        search_params = {
            "dateTime": day,
            "covers": party_size,
            "latitude": lat,
            "longitude": long,
        }

        resp = self._get("s", params=search_params)

        soup = BeautifulSoup(resp.text, "html.parser")

        scripts = soup.find_all("script")

        raw_script = [
            script for script in scripts if "__INITIAL_STATE__" in script.text
        ]

        regex = re.compile(r'JSON\.parse\("(.*)"\)\;')

        res = re.search(regex, raw_script[0].text)

        raw_json = res.group(1)

        json_data = self._santize_json(raw_json)

        return json_data


if __name__ == "__main__":
    from i_need_a_res.geo_util.lib import get_city_geopoint

    today = dt.now()
    pdx = get_city_geopoint("Portland, OR")

    client = OpenTableClient("", "")
    r = client.get_venues(pdx, today, 2)

    pprint(r)
