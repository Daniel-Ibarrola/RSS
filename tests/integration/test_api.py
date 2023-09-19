import datetime
from bs4 import BeautifulSoup
import pytest

from rss.api.config import APIConfig
from rss.services.api_client import APIClient
from rss.cap.alert import Alert


client = APIClient(APIConfig.API_URL)


def post_alerts() -> list[datetime.datetime]:
    date0 = datetime.datetime(year=2023, month=3, day=12)
    date1 = datetime.datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5)
    date2 = datetime.datetime(year=2023, month=3, day=13, hour=16, minute=7, second=10)
    date3 = datetime.datetime(year=2023, month=3, day=14, hour=16, minute=7, second=10)
    # Regions 41201: Petatlan Gro 41204: Guerrero
    # Regions 41215: Zihuatanejo Gro 41216: Guerrero
    alert0 = Alert(date0, [43], 41216, "ALERT0", True)
    alert1 = Alert(date1, [40], 41201, "ALERT1", False)
    alert2 = Alert(date2, [41], 41204, "ALERT2", False)
    alert3 = Alert(date3, [42], 41215, "ALERT3", False)

    client.post_alerts([alert0, alert1, alert2, alert3])

    return [date0, date1, date2, date3]


class TestAlertsAPI:

    @pytest.mark.usefixtures("postgres_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_get_alert_by_id(self):
        dates = post_alerts()
        res = client.get_alert_by_id("ALERT2")
        assert res.ok

        alert_json = {
            "time": dates[2].isoformat(timespec="seconds"),
            "states": [41],
            "region": 41204,
            "is_event": False,
            "id": "ALERT2",
            "references": [],
        }
        assert res.json() == alert_json

    @pytest.mark.usefixtures("postgres_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_alerts_pagination(self):
        dates = post_alerts()
        res = client.get_alerts()
        assert res.ok
        assert res.json() == {
            "alerts": [
                {
                    "time": dates[3].isoformat(timespec="seconds"),
                    "states": [42],
                    "region": 41215,
                    "is_event": False,
                    "id": "ALERT3",
                    "references": [],
                },
                {
                    "time": dates[2].isoformat(timespec="seconds"),
                    "states": [41],
                    "region": 41204,
                    "is_event": False,
                    "id": "ALERT2",
                    "references": [],
                },
                {
                    "time": dates[1].isoformat(timespec="seconds"),
                    "states": [40],
                    "region": 41201,
                    "is_event": False,
                    "id": "ALERT1",
                    "references": [],
                },
                {
                    "time": dates[0].isoformat(timespec="seconds"),
                    "states": [43],
                    "region": 41216,
                    "is_event": True,
                    "id": "ALERT0",
                    "references": [],
                },
            ],
            "prev": None,
            "next": None,
            "count": 4
        }

    @pytest.mark.usefixtures("postgres_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_get_last_alert(self):
        last_alert_date = post_alerts()[-1]

        res = client.get_last_alert()
        assert res.ok
        assert res.json() == {
            "time": last_alert_date.isoformat(timespec="seconds"),
            "states": [42],
            "region": 41215,
            "is_event": False,
            "id": "ALERT3",
            "references": [],
        }


class TestCapFile:

    @pytest.mark.usefixtures("postgres_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_get_cap_file(self):
        dates = post_alerts()
        res = client.get_cap_file(identifier="ALERT2")
        assert res.ok

        contents = BeautifulSoup(res.json()["contents"], "xml")
        assert contents.feed.title.string == "SASMEX-CIRES RSS Feed"

        alert = contents.feed.entry.content.alert
        assert alert.identifier.string == "CIRES_ALERT2"
        assert alert.sent.string == dates[2].isoformat(timespec="seconds") + "-06:00"

    @pytest.mark.usefixtures("postgres_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_get_last_cap_file(self):
        post_alerts()
        res = client.get_cap_file(identifier="latest")
        assert res.ok

        contents = BeautifulSoup(res.json()["contents"], "xml")
        assert contents.feed.title.string == "SASMEX-CIRES RSS Feed"

        alert = contents.feed.entry.content.alert
        assert alert.identifier.string == "CIRES_ALERT3"


class TestAuthentication:

    @pytest.mark.usefixtures("postgres_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_not_logged_user_cannot_post(self):
        alert = Alert(
            time=datetime.datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
            states=[40],
            region=42201,
            is_event=False,
            id="TESTALERT",
        )
        unauthorized_client = APIClient(APIConfig.API_URL)
        unauthorized_client.credentials = ("unknown_user", "dog")
        res = unauthorized_client.post_alert(alert)
        assert res.status_code == 401


class TestAlertFilters:

    @pytest.mark.usefixtures("postgres_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_get_alerts_by_date(self):
        dates = post_alerts()
        start_date = datetime.date(year=2023, month=3, day=13)
        res = client.get_alerts(start_date=start_date)
        assert res.ok
        assert res.json() == {
            "alerts": [
                {
                    "time": dates[1].isoformat(timespec="seconds"),
                    "states": [40],
                    "region": 41201,
                    "is_event": False,
                    "id": "ALERT1",
                    "references": [],
                },
                {
                    "time": dates[2].isoformat(timespec="seconds"),
                    "states": [41],
                    "region": 41204,
                    "is_event": False,
                    "id": "ALERT2",
                    "references": [],
                },
            ]}

    @pytest.mark.usefixtures("postgres_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_get_alerts_in_date_range(self):
        dates = post_alerts()
        start = datetime.date(2023, 3, 11)
        end = datetime.date(2023, 3, 13)
        res = client.get_alerts(start_date=start, end_date=end)
        assert res.ok
        assert res.json() == {
            "alerts": [
                {
                    "time": dates[0].isoformat(timespec="seconds"),
                    "states": [43],
                    "region": 41216,
                    "is_event": True,
                    "id": "ALERT0",
                    "references": [],
                },
                {
                    "time": dates[1].isoformat(timespec="seconds"),
                    "states": [40],
                    "region": 41201,
                    "is_event": False,
                    "id": "ALERT1",
                    "references": [],
                },
                {
                    "time": dates[2].isoformat(timespec="seconds"),
                    "states": [41],
                    "region": 41204,
                    "is_event": False,
                    "id": "ALERT2",
                    "references": [],
                },
            ]
        }

    @pytest.mark.usefixtures("postgres_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_get_event_alerts(self):
        dates = post_alerts()
        res = client.get_alerts(alert_type="event")
        assert res.ok
        assert res.json() == {
            "alerts": [
                {
                    "time": dates[0].isoformat(timespec="seconds"),
                    "states": [43],
                    "region": 41216,
                    "is_event": True,
                    "id": "ALERT0",
                    "references": [],
                },
            ],
            "prev": None,
            "next": None,
            "count": 1
        }

    @pytest.mark.usefixtures("postgres_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_get_alerts(self):
        dates = post_alerts()
        res = client.get_alerts(alert_type="alert")
        assert res.ok
        assert res.json() == {
            "alerts": [
                {
                    "time": dates[3].isoformat(timespec="seconds"),
                    "states": [42],
                    "region": 41215,
                    "is_event": False,
                    "id": "ALERT3",
                    "references": [],
                },
                {
                    "time": dates[2].isoformat(timespec="seconds"),
                    "states": [41],
                    "region": 41204,
                    "is_event": False,
                    "id": "ALERT2",
                    "references": [],
                },
                {
                    "time": dates[1].isoformat(timespec="seconds"),
                    "states": [40],
                    "region": 41201,
                    "is_event": False,
                    "id": "ALERT1",
                    "references": [],
                },
            ],
            "prev": None,
            "next": None,
            "count": 3
        }

    @pytest.mark.usefixtures("postgres_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_get_alerts_by_region(self):
        dates = post_alerts()
        res = client.get_alerts(region="Guerrero")
        assert res.ok
        assert res.json() == {
            "alerts": [
                {
                    "time": dates[2].isoformat(timespec="seconds"),
                    "states": [41],
                    "region": 41204,
                    "is_event": False,
                    "id": "ALERT2",
                    "references": [],
                },
                {
                    "time": dates[0].isoformat(timespec="seconds"),
                    "states": [43],
                    "region": 41216,
                    "is_event": True,
                    "id": "ALERT0",
                    "references": [],
                },
            ],
            "prev": None,
            "next": None,
            "count": 2
        }

    @pytest.mark.usefixtures("postgres_session")
    @pytest.mark.usefixtures("wait_for_api")
    def test_get_alerts_by_state(self):
        dates = post_alerts()
        res = client.get_alerts(state="CDMX")
        assert res.ok
        assert res.json() == {
            "alerts": [
                {
                    "time": dates[1].isoformat(timespec="seconds"),
                    "states": [40],
                    "region": 41201,
                    "is_event": False,
                    "id": "ALERT1",
                    "references": [],
                },
            ],
            "prev": None,
            "next": None,
            "count": 1
        }
