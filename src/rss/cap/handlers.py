from datetime import datetime
import os
import pickle
import queue
import threading
import time
from typing import Optional, Union

from rss import CONFIG
from rss.cap.alert import Alert
from rss.cap.data import POLYGONS
from rss.cap.rss import create_feed, write_feed_to_file
from rss.utils.logger import get_module_logger

logger = get_module_logger(__name__)


class AlertHandler:

    def __init__(self, data_queue: queue.Queue, alerts: Optional[queue.Queue] = None):
        self.queue = data_queue  # type: queue.Queue[bytes]

        self._process_thread = threading.Thread(
            target=self._process_messages, daemon=True
        )
        self._stop = False
        self._cities_queue = []

        self.new_alert_time = CONFIG.ALERT_TIME  # in seconds
        self.wait = 1

        if alerts is None:
            self.alerts = queue.Queue()  # type: queue.Queue[Alert]
        else:
            self.alerts = alerts

    @property
    def process_thread(self) -> threading.Thread:
        return self._process_thread

    @property
    def cities_queue(self) -> list[tuple[int, datetime]]:
        return self._cities_queue

    def _process_messages(self) -> None:
        """ Process messages and create or update alerts.
        """
        while not self._stop:
            msg = self._get_message()
            if msg is not None:
                alert = self._get_alert(msg)
                if alert is not None:
                    self.alerts.put(alert)

            self._flush_cities_queue()
            time.sleep(self.wait)

    def _get_alert(self, msg: bytes) -> Union[Alert, None]:
        """ Get an alert from a message."""
        msg = msg.decode().strip()
        # TODO: update codes for events
        if msg.startswith("84,3") or msg.startswith("84,2"):
            city, region, date = self._parse_message(msg)
            triggered = True if msg.startswith("84,3") else False

            if self._check_city(city):
                alert = Alert(
                    time=date,
                    city=city,
                    region=region,
                    polygons=[POLYGONS[city]],
                    triggered=triggered
                )
                logger.info(f"New alert: {self._alert_str(alert)}")
                self._cities_queue.append((city, date))
                return alert

    def _get_message(self) -> bytes:
        try:
            return self.queue.get(timeout=1)
        except queue.Empty:
            pass

    def _check_city(self, city: int) -> bool:
        """ Checks that the given city is not in the queue"""
        for cty, date in self._cities_queue:
            if city == cty:
                return False
        return True

    def _flush_cities_queue(self) -> None:
        remove = set()
        for ii in range(len(self._cities_queue)):
            if self._time_diff(datetime.now(), self._cities_queue[ii][1]) >= self.new_alert_time:
                remove.add(ii)

        self._cities_queue = [c for ii, c in enumerate(self._cities_queue) if ii not in remove]

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
        self.save_path = CONFIG.SAVE_PATH

        self._process_thread = threading.Thread(target=self._process_alerts, daemon=True)
        self._stop = False
        self.wait = 1
        self.alert_filename = CONFIG.ALERT_FILE_NAME
        self.non_alert_filename = CONFIG.NON_ALERT_FILE_NAME

    @property
    def process_thread(self) -> threading.Thread:
        return self._process_thread

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
                if alert.triggered:
                    filename = self.alert_filename
                else:
                    filename = self.non_alert_filename

                feed_path = os.path.join(self.save_path, f"{filename}_{feed.updated_date}.cap")
                write_feed_to_file(feed_path, feed)
                logger.info(f"Cap file written to {feed_path}")

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
