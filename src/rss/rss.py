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

    def build(self, indentation: str = '\t') -> None:
        """ Creates a string with the contents of the rss feed.
        """
        self._create_header()

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
