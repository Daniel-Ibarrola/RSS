import copy
from datetime import datetime
import os
import queue
import random
import string
import threading
import time
from typing import Optional, Union

from rss import CONFIG
from rss.cap.alert import Alert
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
        self._updates = []  # type: list[Alert]

        self.new_alert_time = CONFIG.ALERT_TIME  # in seconds
        self.wait = 0.1

        if alerts is None:
            self.alerts = queue.Queue()  # type: queue.Queue[Alert]
        else:
            self.alerts = alerts

    @property
    def process_thread(self) -> threading.Thread:
        return self._process_thread

    @property
    def updates(self) -> list[Alert]:
        return self._updates

    def _process_messages(self) -> None:
        """ Process messages and create or update alerts.
        """
        while not self._stop:
            msg = self._get_message()
            if msg is not None:
                alert = self._get_alert(msg)
                if alert is not None:
                    self.alerts.put(alert)
                    self.updates.append(alert)

    def _get_alert(self, msg: bytes) -> Union[Alert, None]:
        """ Get an alert from a message."""
        msg = msg.decode().strip()
        # TODO: update codes for events
        if msg.startswith("84,3") or msg.startswith("84,2"):
            city, region, date = self._parse_message(msg)
            is_event = True if msg.startswith("84,2") else False

            self._flush_updates()
            if self._check_city(city):
                if len(self.updates) == 0:
                    refs = None
                else:
                    refs = copy.deepcopy(self.updates)
                alert = Alert(
                    time=date,
                    city=city,
                    region=region,
                    id=self.alert_id(date),
                    is_event=is_event,
                    refs=refs
                )
                logger.info(f"New alert: {self._alert_str(alert)}")
                return alert

    def _get_message(self) -> bytes:
        try:
            return self.queue.get(timeout=self.wait)
        except queue.Empty:
            pass

    def _check_city(self, city: int) -> bool:
        """ Checks that the given city is not in the queue"""
        return not any(alert.city == city for alert in self.updates)

    def _flush_updates(self) -> None:
        if self.updates:
            diff = self._time_diff(datetime.now(), self.updates[0].time)
            if diff > self.new_alert_time:
                self.updates.clear()

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
    def alert_id(date: datetime) -> str:
        month = f"{date.month:02d}"
        day = f"{date.day:02d}"
        hour = f"{date.hour:02d}"
        minute = f"{date.minute:02d}"
        second = f"{date.second:02d}"
        date = str(date.year) + month + day + hour + minute + second
        random_str = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6))

        return date + "-" + random_str

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
        self.update_filename = CONFIG.UPDATE_FILE_NAME
        self.event_filename = CONFIG.EVENT_FILE_NAME
        self.event_update_filename = CONFIG.EVENT_UPDATE_FILE_NAME

    @property
    def process_thread(self) -> threading.Thread:
        return self._process_thread

    def _process_alerts(self):
        while not self._stop:
            try:
                alert = self.alerts.get(timeout=0.1)
            except queue.Empty:
                time.sleep(self.wait)
                continue

            if alert.is_event and alert.refs is not None:
                filename = self.event_update_filename
            elif alert.is_event and alert.refs is None:
                filename = self.event_filename
            elif not alert.is_event and alert.refs is not None:
                filename = self.update_filename
            else:
                filename = self.alert_filename

            feed = create_feed(alert, is_test=False)

            feed_path = os.path.join(self.save_path, f"{filename}_{feed.updated_date}.cap")
            write_feed_to_file(feed_path, feed)
            logger.info(f"Cap file written to {feed_path}")

    def run(self) -> None:
        self._process_thread.start()

    def join(self) -> None:
        self._process_thread.join()

    def shutdown(self) -> None:
        self._stop = True
        self.join()