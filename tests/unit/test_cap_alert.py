import datetime

from rss.cap.alert import Alert


def test_from_json():
    alert_json = {
        "time": "2023-09-13T15:36:41",
        "states": [40, 41],
        "region": 40101,
        "is_event": False,
        "id": "ALERTID",
        "references": ["ALERTID1", "ALERTID2"]
    }
    expected = Alert(
        time=datetime.datetime(2023, 9, 13, 15, 36, 41),
        states=[40, 41],
        region=40101,
        id="ALERTID",
        is_event=False,
        refs=None
    )
    alert = Alert.from_json(alert_json)
    assert alert == expected
