import datetime

import requests
from rss import CONFIG
from rss.cap.alert import Alert


class APIClient:
    """ Client to post and get alerts from our API"""

    def __init__(self):
        self.base_url = CONFIG.API_URL + "/api/v1"

    def post_alert(self, alert: Alert) -> requests.Response:
        references = []
        if alert.refs is not None:
            references = [ref.id for ref in alert.refs]

        res = requests.post(f"{self.base_url}/new_alert", json={
            "time": alert.time.isoformat(timespec="seconds"),
            "city": alert.city,
            "region": alert.region,
            "is_event": alert.is_event,
            "id": alert.id,
            "references": references,
        })
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
        res = requests.get(f"{self.base_url}/cap/{identifier}")
        return res
