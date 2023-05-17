import requests
from rss import CONFIG
from rss.cap.alert import Alert


class APIClient:
    """ Client to post and get alerts from our API"""

    def __init__(self):
        self.base_url = CONFIG.API_URL

    def post_alert(self, alert: Alert) -> requests.Response:
        res = requests.post(f"{self.base_url}/new_alert", json={
            "time": alert.time.isoformat(timespec="seconds"),
            "city": alert.city,
            "region": alert.region,
            "is_event": alert.is_event,
            "polygons": alert.polygons,
            "id": alert.id,
        })
        return res

