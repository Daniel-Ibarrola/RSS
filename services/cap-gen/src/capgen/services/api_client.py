import datetime
from typing import Literal, Optional

import requests
from rss.cap.alert import Alert
from rss.cap.states import STATES_CODES

from capgen import CONFIG


class APIClient:
    """ Client to post and get alerts from our API"""

    def __init__(self, base_url: str = CONFIG.API_URL):
        self.base_url = base_url + "/api/v1"
        self.credentials = (CONFIG.API_USER, CONFIG.API_PASSWORD)

    def post_alert(self, alert: Alert, save_path: str = "") -> requests.Response:
        """ Post a new alert. """
        references = []
        if alert.refs is not None:
            references = [ref.id for ref in alert.refs]

        url = f"{self.base_url}/alerts/"
        if save_path:
            url += f"?save_path={save_path}"

        res = requests.post(
            url,
            json={
                "time": alert.time.isoformat(timespec="seconds"),
                "states": alert.states,
                "region": alert.region,
                "is_event": alert.is_event,
                "id": alert.id,
                "references": references,
            },
            auth=self.credentials
        )
        return res

    def post_alerts(self, alerts: list[Alert]) -> None:
        for al in alerts:
            res = self.post_alert(al)
            assert res.ok

    def get_alert_by_id(self, identifier: str) -> requests.Response:
        """ Get the alert with the given identifier. """
        return requests.get(f"{self.base_url}/alerts/{identifier}")

    def get_alerts(
            self,
            page: int = None,
            alert_type: Literal["alert", "event", "all"] = "all",
            start_date: Optional[datetime.date] = None,
            end_date: Optional[datetime.date] = None,
            region: str = "",
            state: str = "",
    ) -> requests.Response:
        """ Fetch all alerts of the given page. Accepts multiple filters
        """
        params = {"type": alert_type}
        if page is not None:
            params["page"] = page
        if start_date is not None:
            params["start_date"] = start_date.isoformat()
        if end_date is not None:
            params["end_date"] = end_date.isoformat()
        if region:
            params["region"] = "".join(region.lower().split())
        if state:
            params["state"] = STATES_CODES[state]

        url = f"{self.base_url}/alerts/"
        return requests.get(url, params=params)

    def get_cap_file(self, identifier: str) -> requests.Response:
        """ Returns a response with the contents of the solicited cap file as string"""
        return requests.get(f"{self.base_url}/alerts/{identifier}/cap?save=false")

    def get_last_alert(self) -> requests.Response:
        """ Fetch the last published alert. """
        return requests.get(f"{self.base_url}/alerts/latest/")
