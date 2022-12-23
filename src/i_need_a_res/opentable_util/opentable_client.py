import json
import logging
import re
from datetime import datetime as dt
from pprint import pprint
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from bs4 import BeautifulSoup
from bs4 import ResultSet
from requests import Response
from requests.sessions import Session

from i_need_a_res.geo_util.lib import GeoPoint
from i_need_a_res.opentable_util.lib import OpenTableAuth
from i_need_a_res.opentable_util.lib import OpenTableVenue


OPENTABLE_API_URL = "https://mobile-api.opentable.com/api"

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


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
            timeout=3,
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

    def _has_initial_state_json(self, results_set: ResultSet) -> bool:
        search = [
            result for result in results_set if "__INITIAL_STATE__" in result.text
        ]

        if len(search) > 0:
            return True
        else:
            return False

    def _extract_json_from_html(self, results_set: ResultSet) -> str:
        raw_script = [
            result for result in results_set if "__INITIAL_STATE__" in result.text
        ]
        regex = re.compile(r'JSON\.parse\("(.*)"\)\;')
        search_result = re.search(regex, raw_script[0].text)
        raw_json = search_result.group(1)
        return raw_json

    def get_venues(
        self, geolocation: GeoPoint, search_day: dt, party_size: int
    ) -> List[OpenTableVenue]:
        lat = geolocation.latitude
        long = geolocation.longitude
        day = search_day.strftime("%Y-%m-%dT%H:%M:%S")

        page_number = 4

        search_params = {
            "dateTime": day,
            "covers": party_size,
            "latitude": lat,
            "longitude": long,
            "page": page_number,
        }

        data_list = []

        resp = self._get("s", params=search_params)
        soup = BeautifulSoup(resp.text, "html.parser")
        scripts = soup.find_all("script")

        raw_json = self._extract_json_from_html(scripts)
        json_data = self._santize_json(raw_json)

        data_list.append(json_data)

        pprint(json_data["availability"])

        # while True:
        #     logger.info(f"Getting page {page_number}")
        #     resp = self._get("s", params=search_params)
        #     soup = BeautifulSoup(resp.text, "html.parser")
        #     scripts = soup.find_all("script")

        #     if self._has_initial_state_json(scripts):
        #         if page_number > 10:
        #             break
        #         logger.info(f"Extracting JSON for page {page_number}")
        #         raw_json = self._extract_json_from_html(scripts)

        #         logger.info("Attempting to decode JSON")
        #         try:
        #             json_data = self._santize_json(raw_json)
        #             logger.info("Decode successful!")
        #         except json.decoder.JSONDecodeError:
        #             logger.warning("Unable to decode JSON, skipping this page...")
        #             page_number += 1
        #             search_params["page"] = page_number
        #             continue

        #         logger.info("Adding JSON to data list")
        #         data_list.append(json_data)
        #         page_number += 1
        #         search_params["page"] = page_number
        #         continue
        #     else:
        #         logger.info("No more pages found.")
        #         break

        return data_list


if __name__ == "__main__":
    from i_need_a_res.geo_util.lib import get_city_geopoint

    today = dt.now()
    pdx = get_city_geopoint("Portland, OR")

    client = OpenTableClient("", "")
    r = client.get_venues(pdx, today, 2)

    print(len(r))
