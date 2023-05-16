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
    )
    feed = create_feed(alert, type="test")
    write_feed_to_file("test.xml", feed)
