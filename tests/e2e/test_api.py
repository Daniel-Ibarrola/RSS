from datetime import datetime
import pytest

from rss.api.client import APIClient
from rss.cap.alert import Alert


@pytest.mark.usefixtures("postgres_session")
@pytest.mark.usefixtures("wait_for_api")
def post_and_get_alerts():
    date = datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5)
    alert = Alert(
        time=date,
        city=40,
        region=42201,
        is_event=False,
        polygons=40,
        id="TESTALERT"
    )

    res = client.post_alert(alert)
    assert res.status_code == 201

    res = client.get_alert(date)
    assert res.ok

    assert res.json() == {
        "time": date.isoformat(timespec="seconds"),
        "city": 40,
        "region": 42201,
        "polygons": [40],
        "event": False,
        "id": "TESTALERT",
    }
