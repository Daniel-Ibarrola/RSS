from datetime import datetime
import pytest

from rss.api import db
from rss.api.models import Alert, State, get_alerts_by_type
from rss.cap.alert import Alert as CapAlert


class TestAlertReferences:

    @pytest.mark.usefixtures("sqlite_session")
    def test_get_alert_references(self):
        id_1 = "ALERT_1"
        alert_1 = Alert(
            time=datetime(2023, 5, 17),
            states=[State(state_id=40)],
            region=12205,
            is_event=False,
            identifier=id_1
        )
        db.session.add(alert_1)
        db.session.commit()

        id_2 = "ALERT_2"
        alert_2 = Alert(
            time=datetime(2023, 5, 18),
            states=[State(state_id=41)],
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
            states=[State(state_id=40)],
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


class TestConvertAlert:

    @staticmethod
    def add_alert_with_references() -> tuple[Alert, Alert]:
        date1 = datetime(2023, 5, 17)
        alert1 = Alert(
            time=date1,
            states=[State(state_id=40)],
            region=12205,
            is_event=False,
            identifier="ALERT1"
        )
        db.session.add(alert1)
        db.session.commit()

        date2 = datetime(2023, 5, 18)
        alert2 = Alert(
            time=date2,
            states=[State(state_id=41)],
            region=12203,
            is_event=False,
            identifier="ALERT2",
            references=[alert1]
        )
        db.session.add(alert2)
        db.session.commit()

        return alert1, alert2

    @pytest.mark.usefixtures("sqlite_session")
    def test_to_json(self):
        alert1, alert2 = self.add_alert_with_references()
        json = alert2.to_json()
        assert json == {
            "time": alert2.time.isoformat(timespec="seconds"),
            "states": [41],
            "region": 12203,
            "is_event": False,
            "id": "ALERT2",
            "references": [
                {
                    "time": alert1.time.isoformat(timespec="seconds"),
                    "states": [40],
                    "region": 12205,
                    "is_event": False,
                    "id": "ALERT1",
                    "references": []
                },
            ],
        }

    @pytest.mark.usefixtures("sqlite_session")
    def test_to_cap_alert(self):
        alert1, alert2 = self.add_alert_with_references()
        cap_alert = alert2.to_cap_alert()

        expected = CapAlert(
            time=alert2.time,
            states=[41],
            region=12203,
            id="ALERT2",
            is_event=False,
            refs=[
                CapAlert(
                    time=alert1.time,
                    states=[40],
                    region=12205,
                    id="ALERT1",
                    is_event=False,
                )
            ],
        )
        assert cap_alert == expected


def add_alerts_to_db() -> list[Alert]:
    alert1 = Alert(
        time=datetime(2023, 5, 17, 13, 20, 5),
        states=[State(state_id=40)],
        region=41219,  # Guerrero
        identifier="ALERT1",
        is_event=False,
    )
    alert2 = Alert(
        time=datetime(2023, 5, 17, 13, 20, 15),
        states=[State(state_id=41)],
        region=41220,  # Guerrero
        identifier="ALERT2",
        is_event=False,
    )
    alert3 = Alert(
        time=datetime(2023, 5, 18, 10, 15, 0),
        states=[State(state_id=42)],
        region=42210,  # Oaxaca
        identifier="ALERT3",
        is_event=True,
    )
    alert4 = Alert(
        time=datetime(2023, 5, 19, 10, 15, 0),
        states=[State(state_id=43)],
        region=43204,  # Costa Mich
        identifier="ALERT4",
        is_event=False,
    )
    alerts = [alert1, alert2, alert3, alert4]
    for alert in alerts:
        db.session.add(alert)
    db.session.commit()
    return alerts


class TestGetByDate:

    @pytest.mark.usefixtures("sqlite_session")
    def test_get_by_date(self):
        alert1, alert2, _, _ = add_alerts_to_db()
        alerts = Alert.get_by_date("2023-05-17")
        assert alerts == [alert1, alert2]

    @pytest.mark.usefixtures("sqlite_session")
    def test_get_by_date_range_desc_order(self):
        expected = add_alerts_to_db()[2:]
        expected.reverse()
        start = "2023-05-18"
        end = "2023-05-19"
        alerts = Alert.get_by_date_range(start, end, desc=True)
        assert alerts == expected

    @pytest.mark.usefixtures("sqlite_session")
    def test_get_by_date_range_asc_order(self):
        expected = add_alerts_to_db()[2:]
        start = "2023-05-18"
        end = "2023-05-19"
        alerts = Alert.get_by_date_range(start, end)
        assert alerts == expected


class TestPagination:

    @pytest.fixture
    def set_max_pages(self):
        original = Alert.PER_PAGE
        Alert.PER_PAGE = 2
        yield
        Alert.PER_PAGE = original

    @pytest.mark.usefixtures("sqlite_session")
    def test_get_pagination(self, set_max_pages):
        alert1, alert2, alert3, alert4 = add_alerts_to_db()

        alerts, prev, next_page, total = Alert.get_pagination(1)
        assert alerts == [alert4, alert3]
        assert prev is None
        assert next_page == 2
        assert total == 4

        alerts, prev, next_page, total = Alert.get_pagination(next_page)
        assert alerts == [alert2, alert1]
        assert prev == 1
        assert next_page is None
        assert total == 4


class TestGetAlertByIdentifier:

    @pytest.mark.usefixtures("sqlite_session")
    def test_get_latest_alert(self):
        alerts = add_alerts_to_db()
        latest = Alert.get_by_identifier("latest")
        expected = alerts[-1]
        assert latest == expected

    @pytest.mark.usefixtures("sqlite_session")
    def test_alert_with_identifier_found(self):
        alerts = add_alerts_to_db()
        alert_2 = Alert.get_by_identifier("ALERT2")
        expected = alerts[1]
        assert alert_2 == expected

    @pytest.mark.usefixtures("sqlite_session")
    def test_alert_is_not_found(self):
        add_alerts_to_db()
        not_found = Alert.get_by_identifier("ALERT5")
        assert not_found is None


class TestGetAlertsByType:

    @pytest.mark.usefixtures("sqlite_session")
    def test_get_all(self):
        expected = add_alerts_to_db()
        expected.reverse()
        alerts, prev, next_page,  total = get_alerts_by_type("all", 1)
        assert alerts == expected
        assert prev is None
        assert next_page is None

    @pytest.mark.usefixtures("sqlite_session")
    def test_get_only_alerts(self):
        alert1, alert2, _, alert4 = add_alerts_to_db()
        alerts, prev, next_page, total = get_alerts_by_type("alert", 1)
        assert alerts == [alert4, alert2, alert1]
        assert prev is None
        assert next_page is None

    @pytest.mark.usefixtures("sqlite_session")
    def test_get_events(self):
        expected = add_alerts_to_db()[2]
        alerts, prev, next_page, total = get_alerts_by_type("event", 1)
        assert len(alerts) == 1
        assert alerts[0] == expected
        assert prev is None
        assert next_page is None

    @pytest.mark.usefixtures("sqlite_session")
    def test_invalid_type_raises_error(self):
        alert_type = "earthquake"
        match = f"Invalid alert type {alert_type}"
        with pytest.raises(ValueError, match=match):
            get_alerts_by_type(alert_type, 1)


class TestGetAlertByLocation:

    @pytest.mark.usefixtures("sqlite_session")
    def test_get_by_state_code(self):
        expected = add_alerts_to_db()[1]
        alerts, prev, next_page, total = Alert.get_by_state_code("41")
        assert len(alerts) == 1
        assert alerts[0] == expected
        assert prev is None
        assert next_page is None

    @pytest.mark.usefixtures("sqlite_session")
    def test_get_by_region(self):
        expected = add_alerts_to_db()[:2]
        expected.reverse()
        alerts, prev, next_page, total = Alert.get_by_region("guerrero")
        assert alerts == expected
        assert prev is None
        assert next_page is None
