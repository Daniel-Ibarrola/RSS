import datetime
import os
import sys

from rss.cap.data import POLYGONS
from rss.cap.alert import Alert
from rss.cap.rss import create_feed, write_feed_to_file


if __name__ == "__main__":
    base_path = os.path.dirname(__file__)

    feed_type = "test"
    save_path = os.path.abspath(os.path.join(base_path, "..", "feeds/"))
    if len(sys.argv) > 1:
        feed_type = sys.argv[1]

    valid_types = {"event", "alert", "update", "test"}
    if feed_type not in valid_types:
        raise ValueError(f"Invalid feed type {feed_type}")

    alert = Alert(
        time=datetime.datetime.now(),
        city=40,
        region=41208,
        polygons=[POLYGONS[40]],
    )
    feed = create_feed(alert, type=feed_type)

    write_feed_to_file(os.path.join(save_path, "test.cap"), feed)
    print(f"CAP file written to {save_path}")
