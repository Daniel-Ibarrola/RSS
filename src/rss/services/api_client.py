import datetime

import requests
from rss import CONFIG
from rss.cap.alert import Alert


class APIClient:
    """ Client to post and get alerts from our API"""

    def __init__(self, base_url: str = CONFIG.API_URL):
        self.base_url = base_url + "/api/v1"
        self.credentials = (CONFIG.API_USER, CONFIG.API_PASSWORD)

    def post_alert(self, alert: Alert, save_path: str = "") -> requests.Response:
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
        res = requests.get(f"{self.base_url}/alerts/{identifier}")
        return res

    def get_alerts_by_date(self, date: datetime.date) -> requests.Response:
        res = requests.get(f"{self.base_url}/alerts/dates/{date.isoformat()}")
        return res

    def get_alerts(self, page: int = None) -> requests.Response:
        url = f"{self.base_url}/alerts/"
        if page is not None:
            url += f"?page={page}"
        res = requests.get(f"{self.base_url}/alerts/")
        return res

    def get_cap_file(self, identifier: str) -> requests.Response:
        """ Returns a response with the contents of the solicited cap file as string"""
        res = requests.get(f"{self.base_url}/cap_contents/{identifier}")
        return res

    def get_last_alert(self) -> requests.Response:
        res = requests.get(f"{self.base_url}/last_alert/")
        return res
