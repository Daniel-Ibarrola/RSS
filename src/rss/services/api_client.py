import datetime
import requests
from typing import Literal
from rss import CONFIG
from rss.cap.alert import Alert
from rss.cap.regions import REGION_CODES
from rss.cap.states import STATES_CODES


class APIClient:
    """ Client to post and get alerts from our API"""

    def __init__(self, base_url: str = CONFIG.API_URL):
        self.base_url = base_url + "/api/v1"
        self.credentials = (CONFIG.API_USER, CONFIG.API_PASSWORD)

    def post_alert(self, alert: Alert, save_path: str = "") -> requests.Response:
        """ Post a new alert.
        """
        references = []
        if alert.refs is not None:
            references = [ref.id for ref in alert.refs]

        url = f"{self.base_url}/new_alert"
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

    def get_alerts_by_date(self, date: datetime.date) -> requests.Response:
        """ Get all alerts emitted in the given day
        """
        return requests.get(f"{self.base_url}/alerts/dates/{date.isoformat()}")

    def get_alerts_in_date_range(self, start: datetime.date, end: datetime.date):
        """ Get all alerts that were emitted from the given start date
            to the given end date.
        """
        url = f"{self.base_url}/alerts/date/{start.isoformat()}?end={end.isoformat()}"
        return requests.get(url)

    def get_alerts(
            self,
            page: int = None,
            alert_type: Literal["alert", "event", "all"] = "all"
    ) -> requests.Response:
        """ Fetch all alerts of the given page. If not page is given, the first one
            is fetched.
        """
        url = f"{self.base_url}/alerts/?type={alert_type}"
        if page is not None:
            url += f"&page={page}"
        return requests.get(url)

    def get_cap_file(self, identifier: str) -> requests.Response:
        """ Returns a response with the contents of the solicited cap file as string"""
        return requests.get(f"{self.base_url}/cap_contents/{identifier}")

    def get_last_alert(self) -> requests.Response:
        """ Fetch the last published alert. """
        return requests.get(f"{self.base_url}/last_alert/")

    def get_alerts_by_region(self, region: str, page: int = None) -> requests.Response:
        """Get all the alerts in a given region.

            Note: region name must have no accents
        """
        region = "".join(region.lower().split())
        url = f"{self.base_url}/regions/{region}"
        if page is not None:
            url += f"&page={page}"
        return requests.get(url)

    def get_alerts_by_state(self, state: str, page: int = None) -> requests.Response:
        """Get all the alerts in a given region.
        """
        state_code = STATES_CODES[state]
        url = f"{self.base_url}/regions/{state_code}"
        if page is not None:
            url += f"&page={page}"
        return requests.get(url)
