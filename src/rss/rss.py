import datetime
from xml.dom import minidom

from rss.alert import Alert


class RSSFeed:
    """ Class to write rss files."""

    def __init__(self, alert: Alert):
        self._alert = alert
        self._event_id = self._get_id(alert.time)
        self._updated_date = datetime.datetime.now().isoformat()

        self._root = minidom.Document()

        self._content = ""

    @property
    def content(self) -> str:
        return self._content

    @staticmethod
    def _get_id(date: datetime.datetime) -> str:
        return f"{date.year}{date.month}{date.day}" \
               f"{date.hour}{date.minute}{date.second}"

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

        title = self._alert.time.strftime("%d %b %Y %H:%M:%S") + " Sismo"
        self._add_text_tag(entry, "title", title)

        author = self._root.createElement("author")
        entry.appendChild(author)
        self._add_text_tag(author, "name", "CIRES A.C.")

        coords = str(self._alert.geocoords[0]) + " " + str(self._alert.geocoords[1])
        self._add_text_tag(entry, "georss:point", coords)
        self._add_text_tag(entry, "georss:elev", "0")

        self._add_text_tag(entry, "summary", "Sismo")

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

        text_tags = [
            ("identifier", self._event_id),
            ("sender", "sasmex.net"),
            ("sent", self._alert.time.isoformat()),
            ("status", "Actual"),
            ("msgType", "Alert"),
            ("scope", "Public"),
            ("code", "IPAWSv1.0"),
            ("note", "Requested by=Cires,Activated by=AGG"),
            ("references", f"sasmex.net,{self._event_id},{self._alert.time.isoformat()}")
        ]
        for tag in text_tags:
            self._add_text_tag(alert, tag[0], tag[1])

        return content, alert

    def _create_info_tag(self):

        info = self._root.createElement("info")

        expire_date = self._alert.time + datetime.timedelta(minutes=1)
        text_tags = [
            ("language", "es-MX"),
            ("category", "Geo"),
            ("event", "Sismo"),
            ("responseType", "Prepare"),
            ("urgency", "Past"),
            ("severity", "Major"),
            ("certainty", "Observed"),
            ("effective", self._alert.time.isoformat()),
            ("expires", expire_date.isoformat()),
            ("senderName", "Sistema de Alerta Sísmica Mexicano"),
            ("headline", "Alerta Sísmica"),
            ("description", "SASMEX registró un sismo"),
            ("instruction", "Realice procedimiento en caso de sismo"),
            ("web", "http://sasmex.net"),
            ("contact", "CIRES"),
        ]
        for tag in text_tags:
            self._add_text_tag(info, tag[0], tag[1])

        event_code = self._root.createElement("eventCode")
        self._add_text_tag(event_code, "valueName", "SAME")
        self._add_text_tag(event_code, "value", "EQW")
        info.appendChild(event_code)

        parameter_tags = [
            ("Id", self._event_id),
            ("EAS", "1"),
            ("EventID", "S42212T1678745171458"),
        ]
        for tag in parameter_tags:
            self._add_parameter_tag(info, tag[0], tag[1])

        # Resource tag
        resource = self._root.createElement("resource")
        self._add_text_tag(resource, "resourceDesc", "Image file (GIF)")
        self._add_text_tag(resource, "mimeType", "image/gif")
        self._add_text_tag(resource, "uri", "http://www.sasmex.net/sismos/getAdvisoryImage")
        info.appendChild(resource)

        # Area tag
        area = self._root.createElement("area")
        self._add_text_tag(area, "areaDesc", "Zona de emisión de alerta")
        # TODO: get polygons
        self._add_text_tag(area, "polygon", "16.12,-94.36,18.30,-94.06,16.97,-91.50,15.45,-93.27,16.12,-94.36")

        geocode = self._root.createElement("geocode")
        self._add_text_tag(geocode, "valueName", "SAME")
        self._add_text_tag(geocode, "value", "009000")
        area.appendChild(geocode)

        info.appendChild(area)

        return info

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


def create_feed(alert: Alert, indentation: str = '\t') -> RSSFeed:
    """ Create and rss feed string.

        Parameters
        ----------
        alert : Alert
            The information of the alert.

        indentation : str, default='\t'
            The indentation to use in the feed file
    """
    rss_feed = RSSFeed(alert)
    rss_feed.build(indentation)
    return rss_feed


def write_feed_to_file(filename: str, feed: RSSFeed):
    feed.write(filename)
