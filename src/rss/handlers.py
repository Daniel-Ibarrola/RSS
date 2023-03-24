from datetime import datetime
import os
import pickle
import queue
import threading
import time
from typing import Optional, Union

from rss import CONFIG
from rss.alert import Alert
from rss.data import POLYGONS
from rss.rss import create_feed, write_feed_to_file
from rss.logger import get_module_logger

logger = get_module_logger(__name__)


class AlertHandler:

    def __init__(self, data_queue: queue.Queue, alerts: Optional[queue.Queue] = None):
        self.queue = data_queue  # type: queue.Queue[bytes]

        self._process_thread = threading.Thread(
            target=self._process_messages, daemon=True
        )
        self._stop = False
        self.new_alert_time = CONFIG.ALERT_TIME  # in seconds
        self.wait = 1
        self._last_alert = None

        if alerts is None:
            self.alerts = queue.Queue()  # type: queue.Queue[Alert]
        else:
            self.alerts = alerts

    @property
    def last_alert(self) -> Union[Alert, None]:
        return self._last_alert

    @property
    def process_thread(self) -> threading.Thread:
        return self._process_thread

    def _process_messages(self) -> None:
        """ Process messages and create or update alerts.
        """
        while not self._stop:
            msg = self._get_message()
            if msg is not None:
                self._update_last_alert(msg)

            if self.last_alert is not None and \
                    self._time_diff(datetime.now(), self.last_alert.time) >= self.new_alert_time:
                self.alerts.put(self.last_alert)
                self._last_alert = None

            time.sleep(self.wait)

    def _update_last_alert(self, msg: bytes) -> None:
        """ Update the last alert."""
        msg = msg.decode().strip()
        if msg.startswith("84,3"):
            city, region, date = self._parse_message(msg)

            if self._last_alert is not None:
                time_diff = self._time_diff(self.last_alert.time, date)
            else:
                time_diff = None

            if time_diff is None or time_diff > self.new_alert_time:
                self._last_alert = Alert(
                    time=date, city=city, region=region,
                    polygons=[POLYGONS[city]], geocoords=(0, 0)
                )
                logger.info(f"New alert: {self._alert_str(self.last_alert)}")
            elif self._last_alert.city != city:
                self._last_alert.polygons.append(POLYGONS[city])

    def _get_message(self) -> bytes:
        try:
            return self.queue.get(timeout=1)
        except queue.Empty:
            pass

    @staticmethod
    def _time_diff(date1: datetime, date2: datetime) -> float:
        return abs((date1 - date2).total_seconds())

    @staticmethod
    def _parse_message(msg: str) -> tuple[int, int, datetime]:
        pieces = msg.split(",")
        city, region = int(pieces[2]), int(pieces[3])
        date = datetime.strptime(pieces[4] + "," + pieces[5], "%Y/%m/%d,%H:%M:%S")
        return city, region, date

    @staticmethod
    def _alert_str(alert: Alert) -> str:
        return f"Alert(time={alert.time.isoformat()}, city={alert.city}," \
               f" region={alert.region})"

    def run(self) -> None:
        self._process_thread.start()

    def join(self) -> None:
        self._process_thread.join()

    def shutdown(self) -> None:
        self._stop = True
        self.join()


class FeedWriter:

    def __init__(self, alerts: queue.Queue):
        self.alerts = alerts
        self.save_path = self._get_save_path()

        self._process_thread = threading.Thread(target=self._process_alerts, daemon=True)
        self._stop = False
        self.wait = 1
        self.filename = CONFIG.FEED_FILE_NAME

    @property
    def process_thread(self) -> threading.Thread:
        return self._process_thread

    @staticmethod
    def _get_save_path() -> str:
        base_path = os.path.dirname(__file__)
        return os.path.abspath(os.path.join(base_path, "..", "..", "feeds/"))

    def _process_alerts(self):
        base_path = os.path.dirname(__file__)
        while not self._stop:
            try:
                alert = self.alerts.get(timeout=1)
            except queue.Empty:
                time.sleep(self.wait)
                continue

            write_feed = True
            if CONFIG.CHECK_LAST_ALERT:
                write_feed = self._check_last_alert(alert, self._load_last_alert(base_path))
            else:
                self._save_alert(alert)

            if write_feed:
                feed = create_feed(alert)
                feed_path = os.path.join(self.save_path, f"{self.filename}_{feed.updated_date}.cap")
                write_feed_to_file(feed_path, feed)
                logger.info(f"Feed file written in {feed_path}")

    @staticmethod
    def _check_last_alert(alert1: Alert, alert2: Union[Alert, None]):
        # Check if the last alert written by the other program is the same
        # to avoid writing two repeated files.
        if alert2 is None:
            return True

        if abs((alert1.time - alert2.time).total_seconds()) > 5 \
                or alert1.polygons != alert2.polygons:
            return True

        return False

    @staticmethod
    def _load_last_alert(base_path) -> Union[Alert, None]:
        alert_file = os.path.join(base_path, "alert.pickle")
        if not os.path.exists(alert_file):
            return None

        with open(alert_file, "rb") as fp:
            alert = pickle.load(fp)
        return alert

    @staticmethod
    def _save_alert(alert: Alert) -> None:
        base_path = os.path.dirname(__file__)
        with open(os.path.join(base_path, "alert.pickle"), "wb") as fp:
            pickle.dump(alert, fp)

    def run(self) -> None:
        self._process_thread.start()

    def join(self) -> None:
        self._process_thread.join()

    def shutdown(self) -> None:
        self._stop = True
        self.join()
