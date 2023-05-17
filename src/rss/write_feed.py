import datetime
import os
import sys

from rss.cap.data import POLYGONS
from rss.cap.alert import Alert
from rss.cap.rss import create_feed, write_feed_to_file
from rss.cap.handlers import AlertHandler


if __name__ == "__main__":
    base_path = os.path.dirname(__file__)

    is_test = True
    is_update = False
    is_event = False
    save_path = os.path.abspath(os.path.join(base_path, "..", "feeds/"))
    if len(sys.argv) > 1:
        feed_type = sys.argv[1]
        if feed_type == "update":
            is_test = False
            is_update = True
        elif feed_type == "alert":
            is_test = False
        elif feed_type == "event":
            is_event = True
        elif feed_type == "test":
            pass
        else:
            raise ValueError(f"Invalid feed type {feed_type}")

    date = datetime.datetime.now()
    alert = Alert(
        time=date,
        city=40,
        region=41208,
        polygons=[POLYGONS[40]],
        is_event=is_event,
        id=AlertHandler.alert_id(date)
    )
    feed = create_feed(alert, is_update=is_update, is_test=is_test)

    write_feed_to_file(os.path.join(save_path, "test.cap"), feed)
    print(f"CAP file written to {save_path}")
