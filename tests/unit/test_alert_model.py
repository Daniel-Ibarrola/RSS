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


