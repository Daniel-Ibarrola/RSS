import datetime
import queue

from rss.cap.alert import Alert

from capgen import CONFIG
from capgen.services import FeedPoster


class TestFeedPoster:

    def test_post_alerts(self, mocker):
        mock_post = mocker.patch("capgen.services.api_client.requests.post")

        date = datetime.datetime.now()
        alert = Alert(
            time=date,
            states=[40],
            region=41203,
            id="TESTALERT",
            is_event=False
        )
        alerts = queue.Queue()
        alerts.put(alert)
        poster = FeedPoster(alerts)
        poster._post_alerts()

        assert alerts.empty()

        url = poster.client.base_url
        url += "/alerts/"

        mock_post.assert_called_once_with(
            url,
            json={
                "time": date.isoformat(timespec="seconds"),
                "states": [40],
                "region": 41203,
                "is_event": False,
                "id": "TESTALERT",
                "references": []
            },
            auth=(CONFIG.API_USER, CONFIG.API_PASSWORD)
        )
