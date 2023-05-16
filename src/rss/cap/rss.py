import datetime
import string
import random
from xml.dom import minidom

from rss.cap.alert import Alert
from rss.cap.data import CITIES, get_region


class RSSFeed:
    """ Class to write rss files."""

    def __init__(
            self, alert: Alert,
            type: str = "alert",
            refs: list[tuple[str, datetime.datetime]] = None
    ):
        self._alert = alert
        self._event_id = self._get_id(alert.time)
        self._updated_date = datetime.datetime.now().isoformat()
        self._type = type
        self._refs = refs

        self._root = minidom.Document()
        self._content = ""

    @property
    def content(self) -> str:
        return self._content

    @property
    def updated_date(self) -> str:
        return self._updated_date

    @updated_date.setter
    def updated_date(self, date: str) -> None:
        self._updated_date = date

    @property
    def event_id(self) -> str:
        return self._event_id

    @event_id.setter
    def event_id(self, event: str) -> None:
        self._event_id = event

    @staticmethod
    def _get_id(date: datetime.datetime) -> str:
        month = f"{date.month:02d}"
        day = f"{date.day:02d}"
        hour = f"{date.hour:02d}"
        minute = f"{date.minute:02d}"
        second = f"{date.second:02d}"
        date = str(date.year) + month + day + hour + minute + second
        random_str = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6))

        return date + "-" + random_str

    def _add_text_tag(self, parent, tag_name, text):
        """ Add a tag that contains text"""
        temp = self._root.createElement(tag_name)
        parent.appendChild(temp)

        text_node = self._root.createTextNode(text)
        temp.appendChild(text_node)

    def _add_link_tag(self, parent, ltype, rel, href):
        """ Add a link tag"""
        link = self._root.createElement("link")
        link.setAttribute("type", ltype)
        link.setAttribute("rel", rel)
        link.setAttribute("href", href)

        parent.appendChild(link)

    def _create_header(self):
        """ Create the header and returns the entry tags which store the
            main body.
        """
        feed = self._root.createElement("feed")
        feed.setAttribute("xml:lang", "es-MX")
        feed.setAttribute("xmlns:georss", "http://www.georss.org/georss")
        feed.setAttribute("xmlns", "http://www.w3.org/2005/Atom")
        self._root.appendChild(feed)

        self._add_text_tag(feed, "id", "https://rss.sasmex.net")
        self._add_link_tag(feed, "text/html", "alternate", "https://rss.sasmex.net")
        self._add_link_tag(feed, "application/atom+xml", "self", "https://rss.sasmex.net/sasmex2.xml")

        text_tags = [
            ("title", "SASMEX-CIRES RSS Feed"),
            ("subtitle", "Sistema de Alerta Sísmica Mexicano"),
            ("updated", self._updated_date),
            ("logo", "https://rss.sasmex.net/ciresFeedLogo2b.png"),
            ("icon", "https://rss.sasmex.net/ciresFeedFavicon.ico"),
        ]
        for tag in text_tags:
            self._add_text_tag(feed, tag[0], tag[1])

        author = self._root.createElement("author")
        feed.appendChild(author)
        self._add_text_tag(author, "name", "CIRES A.C.")
        self._add_text_tag(author, "email", "infoCAP@cires-ac.mx")

        entry = self._root.createElement("entry")
        feed.appendChild(entry)
        return entry

    def _create_entry_tag(self, entry):
        """ Creates the 'entry' tag that stores the main body.
        """
        self._add_text_tag(entry, "id", self._event_id)
        self._add_text_tag(entry, "updated", self._updated_date)

        title = self._get_title()
        self._add_text_tag(entry, "title", title)

        author = self._root.createElement("author")
        entry.appendChild(author)
        self._add_text_tag(author, "name", "CIRES A.C.")

    def _add_parameter_tag(self, parent, value_name: str, value: str):
        parameter = self._root.createElement("parameter")
        parent.appendChild(parameter)

        self._add_text_tag(parameter, "valueName", value_name)
        self._add_text_tag(parameter, "value", value)

    def _create_content_tag(self):
        content = self._root.createElement("content")
        content.setAttribute("type", "text/xml")

        alert = self._root.createElement("alert")
        alert.setAttribute("xmlns", "urn:oasis:names:tc:emergency:cap:1.1")
        content.appendChild(alert)

        if self._type == "test":
            status = "Test"
        else:
            status = "Actual"

        sender = "sasmex.net"
        msg_type = "Alert"
        if self._type == "update":
            msg_type = "Update"
        text_tags = [
            ("identifier", self._event_id),
            ("sender", sender),
            ("sent", self._alert.time.isoformat(timespec="seconds") + "-06:00"),
            ("status", status),
            ("msgType", msg_type),
            ("scope", "Public"),
        ]
        for tag in text_tags:
            self._add_text_tag(alert, tag[0], tag[1])

        if self._type == "update" and self._refs is not None:
            references = self._get_references(sender)
            self._add_text_tag(alert, "references", references)

        return content, alert

    def _get_references(self, sender: str) -> str:
        references = ""
        for ii in range(len(self._refs) - 1):
            ref_id = self._refs[ii][0]
            date = self._refs[ii][1].isoformat(timespec="seconds") + "-06:00"
            references += sender + "," + ref_id + "," + date + " "

        ref_id = self._refs[-1][0]
        date = self._refs[-1][1].isoformat(timespec="seconds") + "-06:00"
        references += sender + "," + ref_id + "," + date

        return references

    def _create_info_tag(self):
        info = self._root.createElement("info")
        expire_date = self._alert.time + datetime.timedelta(minutes=1)

        event = "Alerta por sismo"
        severity = "Severe"
        headline = "Alerta Sísmica"
        if self._type == "event":
            event = "Sismo"
            severity = "Minor"
            headline = "Sismo"

        text_tags = [
            ("language", "es-MX"),
            ("category", "Geo"),
            ("event", event),
            ("responseType", "Prepare"),
            ("urgency", "Past"),
            ("severity", severity),
            ("certainty", "Observed"),
            ("effective", self._alert.time.isoformat(timespec="seconds") + "-06:00"),
            ("expires", expire_date.isoformat(timespec="seconds") + "-06:00"),
            ("senderName", "Sistema de Alerta Sísmica Mexicano"),
            ("headline", headline),
            ("description", "SASMEX registró un sismo"),
            ("instruction", "Realice procedimiento en caso de sismo"),
            ("web", "http://sasmex.net"),
            ("contact", "CIRES"),
        ]
        for tag in text_tags:
            self._add_text_tag(info, tag[0], tag[1])

        parameter_tags = [
            ("EAS", "1"),
        ]
        for tag in parameter_tags:
            self._add_parameter_tag(info, tag[0], tag[1])

        # Area tag
        area = self._root.createElement("area")
        self._add_text_tag(area, "areaDesc", "Zona de emisión de alerta")
        self._polygon_tags(area)
        info.appendChild(area)

        return info

    def _get_title(self) -> str:
        title = self._alert.time.strftime("%d %b %Y %H:%M:%S")
        city = CITIES[self._alert.city]
        region = get_region(self._alert.region)
        title += f" Alerta en {city} por sismo en {region}"
        return title

    def _polygon_tags(self, parent):
        for polygon in self._alert.polygons:
            text = ""
            for ii in range(len(polygon.points) - 1):
                point = polygon.points[ii]
                text += f"{point.lat:0.2f},{point.lon:0.2f} "

            # Last point should not have space at the end
            point = polygon.points[-1]
            text += f"{point.lat:0.2f},{point.lon:0.2f}"
            self._add_text_tag(parent, "polygon", text)

    def build(self, indentation: str = '\t') -> None:
        """ Creates a string with the contents of the rss feed.
        """
        entry = self._create_header()
        self._create_entry_tag(entry)

        content_tag, alert_tag = self._create_content_tag()
        info_tag = self._create_info_tag()
        alert_tag.appendChild(info_tag)
        entry.appendChild(content_tag)

        self._content = self._root.toprettyxml(indent=indentation, encoding="UTF-8").decode()

    def write(self, filename: str) -> None:
        """ Write the feed to a file.
        """
        with open(filename, "w") as fp:
            fp.write(self._content)


def create_feed(alert: Alert,
                indentation: str = '\t',
                type: str = "alert"
                ) -> RSSFeed:
    """ Create and rss feed string.

        Parameters
        ----------
        alert : Alert
            The information of the alert.

        indentation : str, default='\t'
            The indentation to use in the feed file

        type : {"event", "alert", "update", "test"}
            If the feed is an event that didn't trigger an alert,
            a new alert, an update of a previous one, or a test.
    """
    rss_feed = RSSFeed(alert, type=type)
    rss_feed.build(indentation)
    return rss_feed


def write_feed_to_file(filename: str, feed: RSSFeed):
    feed.write(filename)
