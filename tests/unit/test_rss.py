from datetime import datetime
from bs4 import BeautifulSoup
import pytest

from rss import CONFIG
from rss.cap import rss
from rss.cap.regions import COORDS
from rss.cap.alert import Alert


class TestRSSFeed:
    @pytest.fixture
    def cap_xml(self):
        alert = Alert(
            time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
            states=[40, 41],
            region=42201,
            is_event=False,
            id="TESTEVENT",
            refs=None
        )
        feed = rss.RSSFeed(alert, is_test=False)
        # We set updated date so we can test it later
        feed.updated_date = datetime(2023, 5, 15, 12, 0, 0).isoformat()

        feed.build()
        data = BeautifulSoup(feed.content, "xml")
        return data

    def test_header_feed_tag(self, cap_xml):
        assert cap_xml.feed.title.string == "SASMEX-CIRES RSS Feed"
        assert cap_xml.feed.updated.string == datetime(2023, 5, 15, 12, 0, 0).isoformat()
        assert len(cap_xml.find_all("alert")) == 1

    def test_entry_title(self, cap_xml):
        title = cap_xml.feed.entry.title
        assert title.string == "13 mar 2023 16:07:05 Alerta en CDMX/Guerrero por sismo en Costa Oax-Gro"

    def test_alert_tag(self, cap_xml):
        alert = cap_xml.feed.entry.content.alert
        sent_time = datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5).\
            isoformat(timespec="seconds") + "-06:00"

        assert alert.identifier.string == "TESTEVENT"
        assert alert.sender.string == "sasmex.net"
        assert alert.sent.string == sent_time
        assert alert.status.string == "Actual"
        assert alert.msgType.string == "Alert"
        assert alert.scope.string == "Public"

    def test_info_tag(self, cap_xml):
        info = cap_xml.feed.entry.alert.info
        effective_date = datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5).\
            isoformat(timespec="seconds") + "-06:00"
        expire_date = datetime(year=2023, month=3, day=13, hour=16, minute=8, second=5).\
            isoformat(timespec="seconds") + "-06:00"

        assert info.language.string == "es-MX"
        assert info.category.string == "Geo"
        assert info.event.string == "Alerta por sismo"
        assert info.responseType.string == "Prepare"
        assert info.urgency.string == "Immediate"
        assert info.severity.string == "Severe"
        assert info.effective.string == effective_date
        assert info.expires.string == expire_date
        assert info.headline.string == "Alerta Sismica"
        assert info.description.string == "SASMEX registro un sismo"
        assert info.instruction.string == "Realice procedimiento en caso de sismo"
        assert info.web.string == "https://rss.sasmex.net"
        assert info.contact.string == "CIRES"

        area = info.area
        assert area.areaDesc.string == "Zona de emision de alerta"

        polygons = area.find_all("polygon")
        assert len(polygons) == 2
        assert polygons[0].string == "17.92,-98.24 19.71,-97.73 20.36,-100.26 18.72,-100.80 17.92,-98.24"
        assert polygons[1].string == "16.01,-98.08 17.84,-97.55 19.29,-101.88 17.73,-102.54 16.01,-98.08"

    @staticmethod
    def sample_alert(refs=None):
        return Alert(
            time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
            states=[42],
            region=42201,
            is_event=False,
            id="TEST_ALERT",
            refs=refs
        )

    def test_create_test_feed(self):
        feed = rss.RSSFeed(alert=self.sample_alert(), is_test=True)
        feed.build()

        data = BeautifulSoup(feed.content, "xml")
        status = data.feed.entry.content.alert.status.string
        assert status == "Test"

    def test_update_feed(self):
        refs = [
            Alert(
                time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
                states=[40],
                region=42201,
                id="REF_ID_1",
                is_event=False,
            ),
            Alert(
                time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=10),
                states=[41],
                region=42201,
                id="REF_ID_2",
                is_event=False,
            ),
        ]
        alert = self.sample_alert(refs)

        feed = rss.RSSFeed(alert=alert, is_test=False)
        feed.build()

        data = BeautifulSoup(feed.content, "xml")
        alert = data.feed.entry.alert
        assert alert.msgType.string == "Update"

        references = alert.references.string.split()
        assert len(references) == 2
        assert references[0] == "sasmex.net,REF_ID_1,2023-03-13T16:07:05-06:00"
        assert references[1] == "sasmex.net,REF_ID_2,2023-03-13T16:07:10-06:00"

        polygons = data.find_all("polygon")
        assert len(polygons) == 3
        assert polygons[0].string == "17.92,-98.24 19.71,-97.73 20.36,-100.26 18.72,-100.80 17.92,-98.24"
        assert polygons[1].string == "16.01,-98.08 17.84,-97.55 19.29,-101.88 17.73,-102.54 16.01,-98.08"
        assert polygons[2].string == "15.48,-94.06 18.35,-93.87 18.55,-98.59 15.62,-98.70 15.48,-94.06"

    def test_event_feed(self):
        region = 42201
        event_alert = Alert(
            time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
            states=[40],
            region=region,
            is_event=True,
            id="TEST_ALERT"
        )
        feed = rss.RSSFeed(alert=event_alert, is_test=False)
        feed.build()

        data = BeautifulSoup(feed.content, "xml")
        assert "Sismo en" in data.feed.entry.title.string

        info = data.feed.entry.alert.info

        assert info.event.string == "Sismo"
        assert info.severity.string == "Minor"
        assert info.headline.string == "Sismo"
        assert info.area.areaDesc.string == "Zona de sismo"

        coords = COORDS[region]
        expected_lat = f"{coords.lat:0.2f}"
        expected_lon = f"{coords.lon:0.2f}"

        circle = info.area.circle.string
        coords, radius = circle.split()

        assert radius == "50.0"
        lat, lon = coords.split(",")
        assert lat == expected_lat
        assert lon == expected_lon


class TestCapFileName:

    def test_event(self):
        event_alert = Alert(
            time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
            states=[40],
            region=41203,
            is_event=True,
            id="TEST_ALERT"
        )
        assert rss.get_cap_file_name(event_alert) == CONFIG.EVENT_FILE_NAME

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
        assert rss.get_cap_file_name(event) == CONFIG.EVENT_UPDATE_FILE_NAME

    def test_alert(self):
        alert = Alert(
            time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
            states=[40],
            region=41203,
            is_event=False,
            id="TEST_ALERT"
        )
        assert rss.get_cap_file_name(alert) == CONFIG.ALERT_FILE_NAME

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
        assert rss.get_cap_file_name(event) == CONFIG.UPDATE_FILE_NAME
