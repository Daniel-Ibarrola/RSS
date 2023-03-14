import datetime
from dataclasses import dataclass
from xml.dom import minidom


@dataclass(frozen=True)
class Location:
    """ Represents the location of the earthquake. """
    name: str
    geocoords: tuple[float, float]
    latitude: float
    longitude: float
    depth: float
    how_far: float


class RSSFeed:
    """ Class to write rss files."""

    def __init__(
        self,
        event_id: str,
        date: datetime.datetime,
        location: Location,
        event: str,
        nearest: str,
        magnitude: float
    ):
        self._event_id = event_id
        self._date = date
        self._location = location
        self._event = event
        self._nearest = nearest
        self._magnitude = magnitude

        self._root = minidom.Document()

        self._content = ""

    @property
    def content(self) -> str:
        return self._content

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
        self._root.appendChild(feed)

        self._add_text_tag(feed, "id", "https://rss.sasmex.net")
        self._add_link_tag(feed, "text/html", "alternate", "https://rss.sasmex.net")
        self._add_link_tag(feed, "application/atom+xml", "self", "https://rss.sasmex.net/sasmex2.xml")

        text_tags = [
            ("title", "SASMEX-Cires Rss Feed"),
            ("subtitle", "Sistema de Alerta Sísmica Mexicano"),
            ("updated", self._date.isoformat()),
            ("logo", "https://rss.sasmex.net/ciresFeedLogo2b.png"),
            ("icon", "https://rss.sasmex.net/ciresFeedFavicon.ico"),
        ]
        for tag in text_tags:
            self._add_text_tag(feed, tag[0], tag[1])

        author = self._root.createElement("author")
        feed.appendChild(author)
        self._add_text_tag(author, "name", "Cires A.C.")
        self._add_text_tag(author, "email", "infoCAP@cires-ac.mx")

        entry_1 = self._root.createElement("entry")
        entry_2 = self._root.createElement("entry")
        feed.appendChild(entry_1)
        feed.appendChild(entry_2)

        return entry_1, entry_2

    def _create_entry_tag(self, entry):
        """ Creates the 'entry' tag that stores the main body.
        """
        self._add_text_tag(entry, "id", "S42212T1678745171458-1678745225150")
        self._add_text_tag(entry, "updated", self._date.isoformat())

        title = self._date.strftime("%d %b %Y %H:%M:%S") + " " + self._event
        title += " en " + self._location.name + " - Actualización"
        self._add_text_tag(entry, "title", title)

        author = self._root.createElement("author")
        entry.appendChild(author)
        self._add_text_tag(author, "name", "Cires A.C.")

        coords = str(self._location.geocoords[0]) + " " + str(self._location.geocoords[1])
        self._add_text_tag(entry, "georss:point", coords)
        self._add_text_tag(entry, "georss:elev", "0")

        self._add_text_tag(entry, "summary", self._event)

    def _add_parameter_tag(self, parent, value_name: str, value: str):
        parameter = self._root.createElement("parameter")
        parent.appendChild(parameter)

        self._add_text_tag(parameter, "valueName", value_name)
        self._add_text_tag(parameter, "value", value)

    def _create_content_tag(self):
        content = self._root.createElement("content")
        content.setAttribute("type", "text/xml")

        alert = self._root.createElement("alert")
        content.appendChild(alert)

        text_tags = [
            ("identifier", "S42212T1678745171458-1678745225150"),
            ("sender", "sasmex.net"),
            ("sent", self._date.isoformat()),
            ("status", "Actual"),
            ("msgType", "Alert"),
            ("scope", "Public"),
            ("references", "sasmex.net,S42212T1678745171458-1678745225148," + self._date.isoformat())
        ]
        for tag in text_tags:
            self._add_text_tag(alert, tag[0], tag[1])

        info = self._root.createElement("info")
        alert.appendChild(info)

        text_tags = [
            ("language", "es-MX"),
            ("category", "Geo"),
            ("event", self._event),
            ("urgency", "Past"),
            ("severity", "Minor"),
            ("certainty", "Observed"),
            ("expires", self._date.isoformat()),
            ("senderName", "Sistema de Alerta Sísmica Mexicano"),
            ("headline", self._event + " en " + self._location.name),
            ("description", self._get_description()),
            ("web", "http://sasmex.net")
        ]
        for tag in text_tags:
            self._add_text_tag(info, tag[0], tag[1])

        parameter_tags = [
            ("Id", "S42212T1678745171458-1678745225150"),
            ("EventID", "S42212T1678745171458"),
            ("layer:Google:Region:0.1", self._location.name),
            ("SsnInfo", "Esperando información")
        ]
        for tag in parameter_tags:
            self._add_parameter_tag(info, tag[0], tag[1])

        area = self._root.createElement("area")
        info.appendChild(area)

        # TODO: some values should not be hardcoded
        descr = f"Sismo Registrado por la estación 42212 Mazatán SV localizada a 25 km al Oeste Suroeste" \
                f" de Salina Cruz, Oaxaca; 55 km al Suroeste de Juchitan, Oaxaca"
        self._add_text_tag(area, "areaDesc", descr)

        coords = str(self._location.geocoords[0]) + "," + str(self._location.geocoords[1]) + " 50.0"
        self._add_text_tag(area, "circle", coords)

        return content

    def _get_description(self):
        return f"El {self._date.strftime('%d %b %Y %H:%M:%S')} el SASMEX registró un sismo que fue evaluado" \
               f" y confirmado por sensores próximos a su epicentro. La estimación de sus " \
               f"efectos es de un {self._event.lower()}. La estación más cercana al epicentro que " \
               f"detectó el sismo es la número {self._nearest}, localizada a 25 km al" \
               f" Oeste Suroeste de {self._location.name}, 55 km al Suroeste de Juchitan, Oaxaca."

    def build(self, indentation: str = '\t') -> None:
        """ Creates a string with the contents of the rss feed.
        """
        entry_1, entry_2 = self._create_header()
        self._create_entry_tag(entry_1)
        self._create_entry_tag(entry_2)

        content_tag_1 = self._create_content_tag()
        content_tag_2 = self._create_content_tag()
        entry_1.appendChild(content_tag_1)
        entry_2.appendChild(content_tag_2)

        self._content = self._root.toprettyxml(indent=indentation)

    def write(self, filename: str) -> None:
        """ Write the feed to a file.
        """
        with open(filename, "w") as fp:
            fp.write(self._content)


def create_feed(
    event_id: str,
    date: datetime.datetime,
    location: Location,
    event: str,
    nearest: str,
    magnitude: float,
    indentation: str = '\t',
) -> RSSFeed:
    """ Create and rss feed string.

        Parameters
        ----------
        event_id : str
            Id of the event

        date : str
            Time when the earthquake occurred.

        location : Location
            The location of the earthquake.

        event : str
            Type of the event. Such as "Sismo ligero".

        nearest : str
            The station nearest to the epicenter.

        magnitude : float
            Magnitude of the earthquake.

        indentation: str, default='\t'
            The indentation to use in the feed file
    """
    rss_feed = RSSFeed(
        event_id, date, location, event, nearest, magnitude
    )
    rss_feed.build(indentation)
    return rss_feed


def write_feed_to_file(filename: str, feed: RSSFeed):
    feed.write(filename)
