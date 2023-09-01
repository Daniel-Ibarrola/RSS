import datetime
from bs4 import BeautifulSoup
import pytest

from rss.services.api_client import APIClient
from rss.cap.alert import Alert


@pytest.mark.usefixtures("postgres_session")
@pytest.mark.usefixtures("wait_for_api")
def test_post_and_get_alerts():
    date1 = datetime.datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5)
    date2 = datetime.datetime(year=2023, month=3, day=13, hour=16, minute=7, second=10)
    alert = Alert(
        time=date1,
        states=[40],
        region=42201,
        is_event=False,
        id="TESTALERT",
    )
    update = Alert(
        time=date2,
        states=[41],
        region=42201,
        is_event=False,
        id="TESTUPDATE",
        refs=[alert]
    )

    client = APIClient()

    res = client.post_alert(alert)
    assert res.status_code == 201

    res = client.post_alert(update)
    assert res.status_code == 201

    res = client.get_alert_by_id("TESTALERT")
    assert res.ok

    alert_json = {
        "time": date1.isoformat(timespec="seconds"),
        "states": [40],
        "region": 42201,
        "is_event": False,
        "id": "TESTALERT",
        "references": [],
    }
    assert res.json() == alert_json

    res = client.get_alert_by_id("TESTUPDATE")
    assert res.ok

    assert res.json() == {
        "time": date2.isoformat(timespec="seconds"),
        "states": [41],
        "region": 42201,
        "is_event": False,
        "id": "TESTUPDATE",
        "references": [alert_json],
    }


def post_alerts(client: APIClient) -> list[datetime.datetime]:
    date1 = datetime.datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5)
    date2 = datetime.datetime(year=2023, month=3, day=13, hour=16, minute=7, second=10)
    date3 = datetime.datetime(year=2023, month=3, day=14, hour=16, minute=7, second=10)
    alert1 = Alert(date1, [40], 41201, "ALERT1", False)
    alert2 = Alert(date2, [41], 41204, "ALERT2", False)
    alert3 = Alert(date3, [42], 41215, "ALERT3", False)

    client.post_alerts([alert1, alert2, alert3])

    return [date1, date2, date3]


@pytest.mark.usefixtures("postgres_session")
@pytest.mark.usefixtures("wait_for_api")
def test_get_alerts_by_date():
    client = APIClient()
    date1, date2, _ = post_alerts(client)

    search_date = datetime.date(year=2023, month=3, day=13)
    res = client.get_alerts_by_date(search_date)
    assert res.ok
    assert res.json() == {
        "alerts": [
            {
                "time": date1.isoformat(timespec="seconds"),
                "states": [40],
                "region": 41201,
                "is_event": False,
                "id": "ALERT1",
                "references": [],
            },
            {
                "time": date2.isoformat(timespec="seconds"),
                "states": [41],
                "region": 41204,
                "is_event": False,
                "id": "ALERT2",
                "references": [],
            },
        ]}


@pytest.mark.usefixtures("postgres_session")
@pytest.mark.usefixtures("wait_for_api")
def test_get_multiple_alerts():
    client = APIClient()
    date1, date2, date3 = post_alerts(client)
    res = client.get_alerts()
    assert res.ok
    assert res.json() == {
        "alerts": [
            {
                "time": date3.isoformat(timespec="seconds"),
                "states": [42],
                "region": 41215,
                "is_event": False,
                "id": "ALERT3",
                "references": [],
            },
            {
                "time": date2.isoformat(timespec="seconds"),
                "states": [41],
                "region": 41204,
                "is_event": False,
                "id": "ALERT2",
                "references": [],
            },
            {
                "time": date1.isoformat(timespec="seconds"),
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
def test_get_cap_file():
    client = APIClient()
    dates = post_alerts(client)

    res = client.get_cap_file(identifier="ALERT2")
    assert res.ok

    contents = BeautifulSoup(res.json()["contents"], "xml")
    assert contents.feed.title.string == "SASMEX-CIRES RSS Feed"

    alert = contents.feed.entry.content.alert
    assert alert.identifier.string == "ALERT2"
    assert alert.sent.string == dates[1].isoformat(timespec="seconds") + "-06:00"


@pytest.mark.usefixtures("postgres_session")
@pytest.mark.usefixtures("wait_for_api")
def test_get_last_cap_file():
    client = APIClient()
    post_alerts(client)

    res = client.get_cap_file(identifier="latest")
    assert res.ok

    contents = BeautifulSoup(res.json()["contents"], "xml")
    assert contents.feed.title.string == "SASMEX-CIRES RSS Feed"

    alert = contents.feed.entry.content.alert
    assert alert.identifier.string == "ALERT3"


@pytest.mark.usefixtures("postgres_session")
@pytest.mark.usefixtures("wait_for_api")
def test_get_last_alerts():
    client = APIClient()
    _, _, last_alert_date = post_alerts(client)

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


@pytest.mark.usefixtures("postgres_session")
@pytest.mark.usefixtures("wait_for_api")
def test_not_logged_user_cannot_post():
    alert = Alert(
        time=datetime.datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
        states=[40],
        region=42201,
        is_event=False,
        id="TESTALERT",
    )
    client = APIClient()
    client.credentials = ("unknown_user", "dog")
    res = client.post_alert(alert)
    assert res.status_code == 401
