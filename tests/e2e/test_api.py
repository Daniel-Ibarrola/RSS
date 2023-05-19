import datetime
import pytest

from rss.api.client import APIClient
from rss.cap.alert import Alert


@pytest.mark.usefixtures("postgres_session")
@pytest.mark.usefixtures("wait_for_api")
def test_post_and_get_alerts():
    date1 = datetime.datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5)
    date2 = datetime.datetime(year=2023, month=3, day=13, hour=16, minute=7, second=10)
    alert = Alert(
        time=date1,
        city=40,
        region=42201,
        is_event=False,
        id="TESTALERT",
    )
    update = Alert(
        time=date2,
        city=41,
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
        "city": 40,
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
        "city": 41,
        "region": 42201,
        "is_event": False,
        "id": "TESTUPDATE",
        "references": [alert_json],
    }


def post_alerts(client: APIClient):
    date1 = datetime.datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5)
    date2 = datetime.datetime(year=2023, month=3, day=13, hour=16, minute=7, second=10)
    date3 = datetime.datetime(year=2023, month=3, day=14, hour=16, minute=7, second=10)
    alert1 = Alert(date1, 40, 12202, "ALERT1", False)
    alert2 = Alert(date2, 41, 12203, "ALERT2", False)
    alert3 = Alert(date3, 42, 12204, "ALERT3", False)

    client.post_alerts([alert1, alert2, alert3])

    return date1, date2, date3


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
                "city": 40,
                "region": 12202,
                "is_event": False,
                "id": "ALERT1",
                "references": [],
            },
            {
                "time": date2.isoformat(timespec="seconds"),
                "city": 41,
                "region": 12203,
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
                "time": date1.isoformat(timespec="seconds"),
                "city": 40,
                "region": 12202,
                "is_event": False,
                "id": "ALERT1",
                "references": [],
            },
            {
                "time": date2.isoformat(timespec="seconds"),
                "city": 41,
                "region": 12203,
                "is_event": False,
                "id": "ALERT2",
                "references": [],
            },
            {
                "time": date3.isoformat(timespec="seconds"),
                "city": 42,
                "region": 12204,
                "is_event": False,
                "id": "ALERT3",
                "references": [],
            },
        ],
        "prev": None,
        "next": None,
        "count": 3
    }
