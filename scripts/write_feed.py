import datetime

from rss.data import POLYGONS
from rss.alert import Alert
from rss.rss import create_feed, write_feed_to_file


if __name__ == "__main__":
    alert = Alert(
        time=datetime.datetime.now(),
        city=40,
        region=41208,
        polygons=[POLYGONS[40]],
        geocoords=(0, 0)
    )
    feed = create_feed(alert)
    write_feed_to_file("test.xml", feed)
