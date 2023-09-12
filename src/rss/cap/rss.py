from babel.dates import format_datetime
import datetime
from xml.dom import minidom

from rss import CONFIG
from rss.cap.alert import Alert
from rss.cap.polygon import STATES, POLYGONS
from rss.cap.regions import COORDS, REGIONS


class UpdateWithNoReferencesError(ValueError):
    pass


class RSSFeed:
    """ Class to write rss files."""

    def __init__(
            self,
            alert: Alert,
            is_test: bool = False,
    ):
        self._alert = alert

        self._is_update = False
        if self._alert.refs is not None:
            self._is_update = True

        self._is_test = is_test
        self._updated_date = datetime.datetime.now().isoformat()
        self._refs = self._alert.refs

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

    def _add_text_tag(
            self, parent: minidom.Element, tag_name: str, text: str
    ) -> None:
        """ Add a tag that contains text"""
        temp = self._root.createElement(tag_name)
        parent.appendChild(temp)

        text_node = self._root.createTextNode(text)
        temp.appendChild(text_node)

    def _add_link_tag(
            self, parent: minidom.Element, ltype: str, rel: str, href: str
    ) -> None:
        """ Add a link tag. """
        link = self._root.createElement("link")
        link.setAttribute("type", ltype)
        link.setAttribute("rel", rel)
        link.setAttribute("href", href)

        parent.appendChild(link)

    def _create_header(self) -> minidom.Element:
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
        self._add_link_tag(feed, "application/atom+xml", "self", "https://rss.sasmex.net/sasmex.xml")

        text_tags = [
            ("title", "SASMEX-CIRES RSS Feed"),
            ("subtitle", "Sistema de Alerta Sismica Mexicano"),
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
        self._add_text_tag(entry, "id", self._alert.id)
        self._add_text_tag(entry, "updated", self._updated_date)

        title = self._get_title()
        self._add_text_tag(entry, "title", title)

        author = self._root.createElement("author")
        entry.appendChild(author)
        self._add_text_tag(author, "name", "CIRES A.C.")

    def _add_parameter_tag(self, parent, value_name: str, value: str) -> None:
        """ Add a parameter tag with the following structure:
            <parameter>
                    <valueName>value_name</valueName>
                    <value>value</value>
            </parameter>
        """
        parameter = self._root.createElement("parameter")
        parent.appendChild(parameter)

        self._add_text_tag(parameter, "valueName", value_name)
        self._add_text_tag(parameter, "value", value)

    def _add_event_code_tag(self, parent, value_name: str, value: str) -> None:
        """ Add a event code tag with the following structure:
            <eventCode>
                    <valueName>value_name</valueName>
                    <value>value</value>
            </eventCode>
        """
        parameter = self._root.createElement("eventCode")
        parent.appendChild(parameter)

        self._add_text_tag(parameter, "valueName", value_name)
        self._add_text_tag(parameter, "value", value)

    def _create_content_and_alert_tag(self) -> tuple[minidom.Element, minidom.Element]:
        """ Creates the content and alert tag.

            The content is the parent of the alert. It just contains the alert.

            The alert is the most important section of the feed. It consists of some metadata,
            namely, identifier, sender, sent, status, msg type and scope and also contains
            the info tag, which contains the alert information. This method does not
            create the info tag, it just adds the metadata.

        """
        content = self._root.createElement("content")
        content.setAttribute("type", "text/xml")

        alert = self._root.createElement("alert")
        alert.setAttribute("xmlns", "urn:oasis:names:tc:emergency:cap:1.1")
        content.appendChild(alert)

        status = "Actual"
        if self._is_test:
            status = "Test"

        sender = "cires.org.mx"
        msg_type = "Alert"
        if self._is_update:
            msg_type = "Update"

        text_tags = [
            ("identifier", "CIRES_" + self._alert.id),
            ("sender", sender),
            ("sent", self._alert.time.isoformat(timespec="seconds") + "-06:00"),
            ("status", status),
            ("msgType", msg_type),
            ("scope", "Public"),
        ]
        for tag in text_tags:
            self._add_text_tag(alert, tag[0], tag[1])

        if self._is_update:
            references = self._get_references(sender)
            self._add_text_tag(alert, "references", references)

        return content, alert

    def _get_references(self, sender: str) -> str:
        """ Get the list of references for an update as a single string
            where each reference is separated by a space.

            A reference has the following format:
                sender,refID,date

            If there are multiple references a string with the following format
            is returned:
                sender,refID_1,date_1 sender,refID_2,date_2
        """
        references = ""
        for ii in range(len(self._refs) - 1):
            ref_id = self._refs[ii].id
            date = self._refs[ii].time.isoformat(timespec="seconds") + "-06:00"
            references += sender + "," + ref_id + "," + date + " "

        ref_id = self._refs[-1].id
        date = self._refs[-1].time.isoformat(timespec="seconds") + "-06:00"
        references += sender + "," + ref_id + "," + date

        return references

    def _create_info_tag(self) -> minidom.Element:
        """ Create the info tag.

            This is a subtag of the alert tag, it contains the most important information
            such as the area, severity, etc.
        """
        info = self._root.createElement("info")
        expire_date = self._alert.time + datetime.timedelta(minutes=1)

        region = REGIONS[self._alert.region]
        distance = 100  # TODO: calculate distance
        states = self._get_states()

        if not self._alert.is_event:
            event = f"SASMEX: ALERTA SISMICA en {states} por sismo en {region}"
            severity = "Severe"
            headline = f"ALERTA SISMICA por sismo Severo en {region}"
            description = f"Sismo Severo en {region}, a {distance}km de {states}"
            response_type = "Execute"
        else:
            event = f"SASMEX: Sismo Moderado en {region}"
            severity = "Unknown"
            headline = f"Sismo Moderado en {region}"
            description = f"Sismo Moderado en {region}, a {distance}km de {states}"
            response_type = "Monitor"

        text_tags = [
            ("language", "es-MX"),
            ("category", "Geo"),
            ("event", event),
            ("responseType", response_type),
            ("urgency", "Immediate"),
            ("severity", severity),
            ("certainty", "Observed"),
            ("effective", self._alert.time.isoformat(timespec="seconds") + "-06:00"),
            ("expires", expire_date.isoformat(timespec="seconds") + "-06:00"),
            ("senderName", "SASMEX - CIRES"),
            ("headline", headline),
            ("description", description),
            ("instruction", "Realice procedimiento en caso de sismo"),
            ("web", "https://rss.sasmex.net"),
            ("contact", "infoCAP@cires-ac.mx"),
        ]
        for tag in text_tags:
            self._add_text_tag(info, tag[0], tag[1])

        self._add_event_code_tag(info, "SAME", "EQW")
        self._add_parameter_tag(info, "SAME", "CIV")

        # Area tag
        area = self._create_area_tag()
        info.appendChild(area)
        return info

    def _create_area_tag(self) -> minidom.Element:
        """ Creates the area tag.

            If the event is an alert, the area is one or multiple polygons
            of the affected cities.

            If the event is not an alert, the area is a circle centered in the
            region of the earthquake.
        """
        area = self._root.createElement("area")
        if self._alert.is_event:
            area_desc = "Zona Probable Epicentro"
        else:
            area_desc = "Region de Alertamiento"

        self._add_text_tag(area, "areaDesc", area_desc)

        if self._alert.is_event:
            self._circle_tag(area)
        else:
            self._polygon_tags(area)
        return area

    def _get_title(self) -> str:
        """ Returns the title of the feed.
        """
        title = format_datetime(self._alert.time, locale="es_MX")
        region = REGIONS[self._alert.region]
        if self._alert.is_event:
            title += f" Sismo en {region}"
        else:
            title += f" Alerta en {self._get_states()} por sismo en {region}"
        return title

    def _get_states(self) -> str:
        """ Returns the states of the alert as a string with the
            following format:
                state1/state2/.../stateN
        """
        state_list = [STATES[s] for s in self._alert.states]
        return "/".join(state_list)

    def _polygon_tags(self, parent: minidom.Element) -> None:
        """ Add the polygons tags that describes the area of alerting.

            A polygon has the following format:

                <polygon>lat1,lon1 lat2,lon2, lat3,lon3, lat4,lon4, lat5,lon5</polygon>
        """
        polygons = []
        # First the references of polygons if any
        if self._refs is not None:
            for ref in self._refs:
                for state in ref.states:
                    polygons.append(POLYGONS[state])
        polygons.extend(POLYGONS[p] for p in self._alert.states)

        for poly in polygons:
            text = ""
            for ii in range(len(poly.points) - 1):
                point = poly.points[ii]
                text += f"{point.lat:0.2f},{point.lon:0.2f} "

            # Last point should not have space at the end
            point = poly.points[-1]
            text += f"{point.lat:0.2f},{point.lon:0.2f}"
            self._add_text_tag(parent, "polygon", text)

    def _circle_tag(self, parent: minidom.Element) -> None:
        """ Add a circle tag to describe the epicenter region of an earthquake.

            It has the following format:

                <circle>lat,lon radius</circle>
        """
        coords = COORDS[self._alert.region]
        text = f"{coords.lat:0.2f},{coords.lon:0.2f} 50.0"
        self._add_text_tag(parent, "circle", text)

    def build(self, indentation: str = '\t') -> None:
        """ Creates a string with the contents of the rss feed.
        """
        entry = self._create_header()
        self._create_entry_tag(entry)

        content_tag, alert_tag = self._create_content_and_alert_tag()
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
                is_test: bool = False,
                indentation: str = '\t',
                ) -> RSSFeed:
    """ Create and rss feed string.

        Parameters
        ----------
        alert : Alert
            The information of the alert.

        is_test : bool
            Whether the created feed is a test.

        indentation : str, default='\t'
            The indentation to use in the feed file

    """
    rss_feed = RSSFeed(alert, is_test)
    rss_feed.build(indentation)
    return rss_feed


def write_feed_to_file(filename: str, feed: RSSFeed):
    feed.write(filename)


def get_cap_file_name(alert: Alert) -> str:
    if alert.is_event and alert.refs is not None:
        return CONFIG.EVENT_UPDATE_FILE_NAME
    elif alert.is_event and alert.refs is None:
        return CONFIG.EVENT_FILE_NAME
    elif not alert.is_event and alert.refs is not None:
        return CONFIG.UPDATE_FILE_NAME
    else:
        return CONFIG.ALERT_FILE_NAME
