from datetime import datetime
import pytest

from rss.api.client import APIClient
from rss.cap.alert import Alert


@pytest.mark.usefixtures("postgres_session")
@pytest.mark.usefixtures("wait_for_api")
def test_post_and_get_alerts():
    date1 = datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5)
    date2 = datetime(year=2023, month=3, day=13, hour=16, minute=7, second=10)
    alert = Alert(
        time=date1,
        city=40,
        region=42201,
        is_event=False,
        id="TESTALERT"
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

    assert res.json() == {
        "time": date1.isoformat(timespec="seconds"),
        "city": 40,
        "region": 42201,
        "is_event": False,
        "id": "TESTALERT",
    }

    res = client.get_alert_by_id("TESTUPDATE")
    assert res.ok

    assert res.json() == {
        "time": date2.isoformat(timespec="seconds"),
        "city": 41,
        "region": 42201,
        "is_event": False,
        "id": "TESTEVENT",
        "refs": ["TESTALERT"],
    }

