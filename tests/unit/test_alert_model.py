from datetime import datetime
import pytest
from rss.api import db
from rss.api.models import Alert


@pytest.mark.usefixtures("sqlite_session")
def test_get_alert_references():
    id_1 = "ALERT_1"
    alert_1 = Alert(
        time=datetime(2023, 5, 17),
        city=40,
        region=12205,
        is_event=False,
        identifier=id_1
    )
    db.session.add(alert_1)
    db.session.commit()

    id_2 = "ALERT_2"
    alert_2 = Alert(
        time=datetime(2023, 5, 18),
        city=41,
        region=12203,
        is_event=False,
        identifier=id_2
    )
    alert_2.references.append(alert_1)
    db.session.add(alert_2)
    db.session.commit()

    references = Alert.get_references([id_1, id_2])
    alert_3 = Alert(
        time=datetime(2023, 5, 18),
        city=42,
        region=12211,
        is_event=False,
        identifier="ALERT_3",
        references=references
    )
    db.session.add(alert_3)
    db.session.commit()

    refs = alert_3.references
    assert len(refs) == 2
    assert refs[0].identifier == id_1
    assert refs[1].identifier == id_2


@pytest.mark.usefixtures("sqlite_session")
def test_to_json():
    date1 = datetime(2023, 5, 17)
    alert1 = Alert(
        time=date1,
        city=40,
        region=12205,
        is_event=False,
        identifier="ALERT1"
    )
    db.session.add(alert1)
    db.session.commit()

    date2 = datetime(2023, 5, 18)
    alert2 = Alert(
        time=date2,
        city=41,
        region=12203,
        is_event=False,
        identifier="ALERT2",
        references=[alert1]
    )
    db.session.add(alert2)
    db.session.commit()

    json = alert2.to_json()
    assert json == {
        "time": date2.isoformat(timespec="seconds"),
        "city": 41,
        "region": 12203,
        "is_event": False,
        "id": "ALERT2",
        "references": [
            {
                "time": date1.isoformat(timespec="seconds"),
                "city": 40,
                "region": 12205,
                "is_event": False,
                "id": "ALERT1",
                "references": []
            },
        ],
    }


def add_alerts_to_db():
    alert1 = Alert(
        time=datetime(2023, 5, 17, 13, 20, 5),
        city=40,
        region=12202,
        identifier="ALERT1",
        is_event=False,
    )
    alert2 = Alert(
        time=datetime(2023, 5, 17, 13, 20, 15),
        city=41,
        region=12202,
        identifier="ALERT2",
        is_event=False,
    )
    alert3 = Alert(
        time=datetime(2023, 5, 18, 10, 15, 0),
        city=42,
        region=12202,
        identifier="ALERT3",
        is_event=True,
    )
    alert4 = Alert(
        time=datetime(2023, 5, 19, 10, 15, 0),
        city=43,
        region=12202,
        identifier="ALERT4",
        is_event=False,
    )
    alerts = [alert1, alert2, alert3, alert4]
    for alert in alerts:
        db.session.add(alert)
    db.session.commit()
    return alerts


@pytest.mark.usefixtures("sqlite_session")
def test_get_by_date():
    alert1, alert2, _, _ = add_alerts_to_db()
    alerts = Alert.get_by_date("2023-05-17")
    assert alerts == [alert1, alert2]


@pytest.mark.usefixtures("sqlite_session")
def test_get_pagination():
    Alert.PER_PAGE = 2
    alert1, alert2, alert3, alert4 = add_alerts_to_db()

    alerts, prev, next_page, total = Alert.get_pagination(1)
    assert alerts == [alert1, alert2]
    assert prev is None
    assert next_page == 2
    assert total == 2

    alerts, prev, next_page, total = Alert.get_pagination(next_page)
    assert alerts == [alert3, alert4]
    assert prev == 1
    assert next_page is None
    assert total == 2
