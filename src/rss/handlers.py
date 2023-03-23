from datetime import datetime
import os
import queue
import threading
import time
from typing import Optional

from rss.alert import Alert
from rss.data import POLYGONS
from rss.rss import create_feed, write_feed_to_file

# TODO: get correct polygons


class AlertHandler:

    def __init__(self, data_queue: queue.Queue, alerts: Optional[queue.Queue] = None):
        self.queue = data_queue  # type: queue.Queue[bytes]

        self._process_thread = threading.Thread(
            target=self._process_messages, daemon=True
        )
        self._stop = False
        self.new_alert_time = 60  # in seconds
        self._wait = 1
        # Initialize to alert with old date and fake city
        self._last_alert = Alert(
            time=datetime(2020, 1, 1), city=-1, region=41203, polygons=[], geocoords=(0, 0)
        )

        if alerts is None:
            self.alerts = queue.Queue()  # type: queue.Queue[Alert]
        else:
            self.alerts = alerts

    def _process_messages(self):
        while not self._stop:
            msg = self._get_message()
            if msg is not None:
                self._create_alert(msg)
            time.sleep(self._wait)

    def _create_alert(self, msg: bytes) -> None:
        msg = msg.decode().strip()
        if msg.startswith("84,3"):
            city, region, date = self._parse_message(msg)
            time_diff = abs((self._last_alert.time - date).total_seconds())
            if time_diff > self.new_alert_time:
                # TODO: get geocoords
                # TODO: put alerts in queue only when enough time has passed
                self._last_alert = Alert(
                    time=date, city=city, region=region,
                    polygons=[POLYGONS[city]], geocoords=(0, 0)
                )
                self.alerts.put(self._last_alert)
            elif self._last_alert.city != city:
                self._last_alert.polygons.append(POLYGONS[city])

    def _get_message(self) -> bytes:
        try:
            return self.queue.get(timeout=1)
        except queue.Empty:
            pass

    @staticmethod
    def _parse_message(msg: str) -> tuple[int, int, datetime]:
        pieces = msg.split(",")
        city, region = int(pieces[2]), int(pieces[3])
        date = datetime.strptime(pieces[4] + "," + pieces[5], "%Y/%m/%d,%H:%M:%S")
        return city, region, date

    def run(self):
        self._process_thread.start()

    def join(self):
        self._process_thread.join()

    def shutdown(self):
        self._stop = True
        self.join()


class FeedWriter:

    def __init__(self, alerts: queue.Queue):
        self.alerts = alerts
        self.save_path = self._get_save_path()

    @staticmethod
    def _get_save_path() -> str:
        base_path = os.path.dirname(__file__)
        return os.path.abspath(os.path.join(base_path, "..", "..", "feeds/"))

    def _process_alert(self, alert: Alert):
        feed = create_feed(alert)
        write_feed_to_file(
            os.path.join(self.save_path, f"sasmex_{feed.updated_date}.rss"),
            feed
        )
