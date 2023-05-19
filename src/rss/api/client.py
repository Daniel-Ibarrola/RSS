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

    def get_alert_by_id(self, identifier: str) -> requests.Response:
        res = requests.get(f"{self.base_url}/alerts/{identifier}")
        return res
