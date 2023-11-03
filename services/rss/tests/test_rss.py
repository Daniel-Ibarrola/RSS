from datetime import datetime
from bs4 import BeautifulSoup
import pytest

from rss.cap import rss
from rss.cap.regions import REGION_COORDS
from rss.cap.alert import Alert


class TestCapAlert:
    @pytest.fixture
    def cap_xml(self):
        alert = Alert(
            time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
            states=[40, 41],
            region=42201,
            is_event=False,
            id="TEST-ALERT",
            refs=None
        )
        feed = rss.RSSFeed(alert, is_test=False)
        # We set updated date so we can test it later
        feed.updated_date = datetime(2023, 5, 15, 12, 0, 0).isoformat()

        feed.build()
        return BeautifulSoup(feed.content, "xml")

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

        assert alert.identifier.string == "CIRES_TEST-ALERT"
        assert alert.sender.string == "cires.org.mx"
        assert alert.sent.string == sent_time
        assert alert.status.string == "Actual"
        assert alert.msgType.string == "Alert"
        assert alert.scope.string == "Public"

    def test_info_tag(self, cap_xml):
        info = cap_xml.feed.entry.alert.info
        expire_date = datetime(year=2023, month=3, day=13, hour=16, minute=8, second=5).\
            isoformat(timespec="seconds") + "-06:00"

        assert info.language.string == "es-MX"
        assert info.category.string == "Geo"
        assert info.event.string == "SASMEX: ALERTA SISMICA en CDMX/Guerrero por sismo en Costa Oax-Gro"
        assert info.responseType.string == "Execute"
        assert info.urgency.string == "Immediate"
        assert info.severity.string == "Severe"
        assert info.certainty.string == "Observed"

        event_code = info.eventCode
        assert event_code.valueName.string == "SAME"
        assert event_code.value.string == "EQW"

        assert info.expires.string == expire_date
        assert info.senderName.string == "SASMEX - CIRES"
        assert info.headline.string == "ALERTA SISMICA por sismo Severo en Costa Oax-Gro"
        assert info.description.string == "Sismo Severo en Costa Oax-Gro, a 347km de CDMX y a 126km de Guerrero"
        assert info.instruction.string == "Realice procedimiento en caso de sismo"
        assert info.web.string == "https://rss.sasmex.net"
        assert info.contact.string == "infoCAP@cires-ac.mx"

        parameter = info.parameter
        assert parameter.valueName.string == "SAME"
        assert parameter.value.string == "CIV"

    def test_area_tag(self, cap_xml):
        info = cap_xml.feed.entry.alert.info
        area = info.area
        assert area.areaDesc.string == "Region de Alertamiento"

        polygons = area.find_all("polygon")
        assert len(polygons) == 2
        assert polygons[0].string == "19.15,-98.95 19.60,-98.95 19.60,-99.35 19.15,-99.35 19.15,-98.95"
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
        assert references[0] == "cires.org.mx,CIRES_REF_ID_1,2023-03-13T16:07:05-06:00"
        assert references[1] == "cires.org.mx,CIRES_REF_ID_2,2023-03-13T16:07:10-06:00"

        polygons = data.find_all("polygon")
        assert len(polygons) == 3
        assert polygons[0].string == "19.15,-98.95 19.60,-98.95 19.60,-99.35 19.15,-99.35 19.15,-98.95"
        assert polygons[1].string == "16.01,-98.08 17.84,-97.55 19.29,-101.88 17.73,-102.54 16.01,-98.08"
        assert polygons[2].string == "15.48,-94.06 18.35,-93.87 18.55,-98.59 15.62,-98.70 15.48,-94.06"


class TestCapEvent:

    @pytest.fixture
    def cap_event_xml(self):
        event_alert = Alert(
            time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
            states=[40],
            region=42201,
            is_event=True,
            id="TEST-EVENT"
        )
        feed = rss.RSSFeed(alert=event_alert, is_test=False)
        feed.build()

        return BeautifulSoup(feed.content, "xml")

    def test_header_tag(self, cap_event_xml):
        assert cap_event_xml.feed.title.string == "SASMEX-CIRES RSS Feed"
        assert len(cap_event_xml.find_all("alert")) == 1

    def test_entry_title(self, cap_event_xml):
        title = cap_event_xml.feed.entry.title
        assert title.string == "13 mar 2023 16:07:05 Sismo en Costa Oax-Gro"

    def test_alert_tag(self, cap_event_xml):
        alert = cap_event_xml.feed.entry.content.alert
        sent_time = datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5). \
                        isoformat(timespec="seconds") + "-06:00"

        assert alert.identifier.string == "CIRES_TEST-EVENT"
        assert alert.sender.string == "cires.org.mx"
        assert alert.sent.string == sent_time
        assert alert.status.string == "Actual"
        assert alert.msgType.string == "Alert"
        assert alert.scope.string == "Public"

    def test_info_tag(self, cap_event_xml):
        info = cap_event_xml.feed.entry.alert.info
        expire_date = datetime(year=2023, month=3, day=13, hour=16, minute=8, second=5). \
                          isoformat(timespec="seconds") + "-06:00"

        assert info.language.string == "es-MX"
        assert info.category.string == "Geo"
        assert info.event.string == "SASMEX: Sismo Moderado en Costa Oax-Gro"
        assert info.responseType.string == "Monitor"
        assert info.urgency.string == "Immediate"
        assert info.severity.string == "Unknown"
        assert info.certainty.string == "Observed"

        event_code = info.eventCode
        assert event_code.valueName.string == "SAME"
        assert event_code.value.string == "EQW"

        assert info.expires.string == expire_date
        assert info.senderName.string == "SASMEX - CIRES"
        assert info.headline.string == "Sismo Moderado en Costa Oax-Gro"
        assert info.description.string == "Sismo Moderado en Costa Oax-Gro, a 347km de CDMX"
        assert info.instruction.string == "Realice procedimiento en caso de sismo"
        assert info.web.string == "https://rss.sasmex.net"
        assert info.contact.string == "infoCAP@cires-ac.mx"

        parameter = info.parameter
        assert parameter.valueName.string == "SAME"
        assert parameter.value.string == "CIV"

    def test_area_tag(self, cap_event_xml):
        info = cap_event_xml.feed.entry.alert.info
        area = info.area
        assert area.areaDesc.string == "Zona Probable Epicentro"

        circle = area.circle.string
        coords, radius = circle.split()

        expected_coords = REGION_COORDS[42201]
        expected_lat = f"{expected_coords.lat:0.2f}"
        expected_lon = f"{expected_coords.lon:0.2f}"

        assert radius == "70.0"
        lat, lon = coords.split(",")
        assert lat == expected_lat
        assert lon == expected_lon
