from datetime import datetime

from rss.cap.alert import Alert

from capgen import CONFIG
from capgen.services.feed_writer import get_cap_file_name


class TestCapFileName:

    def test_event(self):
        event_alert = Alert(
            time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
            states=[40],
            region=41203,
            is_event=True,
            id="TEST_ALERT"
        )
        assert get_cap_file_name(event_alert) == CONFIG.EVENT_FILE_NAME

    def test_event_update(self):
        references = [
            Alert(
                time=datetime(year=2023, month=3, day=13, hour=16, minute=6, second=5),
                states=[40],
                region=41205,
                is_event=True,
                id="TEST_ALERT"
            )
        ]
        event = Alert(
            time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
            states=[40],
            region=41203,
            is_event=True,
            id="TEST_ALERT",
            refs=references
        )
        assert get_cap_file_name(event) == CONFIG.EVENT_UPDATE_FILE_NAME

    def test_alert(self):
        alert = Alert(
            time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
            states=[40],
            region=41203,
            is_event=False,
            id="TEST_ALERT"
        )
        assert get_cap_file_name(alert) == CONFIG.ALERT_FILE_NAME

    def test_alert_update(self):
        references = [
            Alert(
                time=datetime(year=2023, month=3, day=13, hour=16, minute=6, second=5),
                states=[40],
                region=41205,
                is_event=False,
                id="TEST_ALERT"
            )
        ]
        event = Alert(
            time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
            states=[40],
            region=41203,
            is_event=False,
            id="TEST_ALERT",
            refs=references
        )
        assert get_cap_file_name(event) == CONFIG.UPDATE_FILE_NAME
