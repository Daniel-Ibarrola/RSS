import abc
import copy
from datetime import datetime
import os
import queue
import random
import string
import threading
from typing import Optional, Union

from rss import CONFIG
from rss.api.client import APIClient
from rss.cap.alert import Alert
from rss.cap.rss import create_feed, write_feed_to_file, get_cap_file_name
from rss.utils.logger import get_module_logger

logger = get_module_logger(__name__)


class AbstractService(abc.ABC):
    """ Abstract base class for all services.

        To add a new service implement the _handle_event method
    """
    def __init__(self):
        # Main thread of this service
        self._process_thread = threading.Thread(
            target=self._handle_event,
            daemon=True
        )
        self._stop = False

    @property
    def process_thread(self) -> threading.Thread:
        return self._process_thread

    @abc.abstractmethod
    def _handle_event(self):
        raise NotImplementedError

    def run(self) -> None:
        self._process_thread.start()
        logger.debug(f"Started {self.__class__.__name__}")

    def join(self) -> None:
        self._process_thread.join()

    def shutdown(self) -> None:
        self._stop = True
        self.join()
        logger.debug(f"Shutting down {self.__class__.__name__}")

    @staticmethod
    def _get_from_queue(data_queue: queue, timeout: float) -> Union[Alert, None]:
        """ Get an item from the queue. If timeout expires and there is
            nothing in the queue returns None.
        """
        try:
            return data_queue.get(timeout=timeout)
        except queue.Empty:
            pass


class MessageProcessor(AbstractService):
    """ Receives alert messages and if they are valid, converts them to an
        Alert object that can be used to create cap feeds.

        Alert msg format:

        84,3,Event/Alert,City1/City2/.../CityN,Station,yyyy/mm/dd,hh:mm:ss,hourMsg\r\n

        Where

        Event/Alert = 0 for events. 1 for alerts
        hourMsg = unix time the message was sent
    """

    def __init__(self, data_queue: queue.Queue, alerts: Optional[queue.Queue] = None):
        super().__init__()
        self.queue = data_queue  # type: queue.Queue[bytes]
        self._updates = []  # type: list[Alert]

        self.new_alert_time = CONFIG.ALERT_TIME  # in seconds
        self.wait = 0.1

        self.alerts = alerts
        if alerts is None:
            self.alerts = queue.Queue()  # type: queue.Queue[Alert]

    @property
    def updates(self) -> list[Alert]:
        return self._updates

    def _handle_event(self) -> None:
        """ Get new messages and create or update alerts.
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
        if msg.startswith("84,3"):
            states, region, date, is_event = self._parse_message(msg)

            self._flush_updates()
            if all(self._check_state(s) for s in states):
                if len(self.updates) == 0:
                    refs = None
                else:
                    refs = copy.deepcopy(self.updates)
                alert = Alert(
                    time=date,
                    states=states,
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

    def _check_state(self, state: int) -> bool:
        """ Checks that the given state is not in the queue"""
        return not any(s == state for alert in self.updates for s in alert.states)

    def _flush_updates(self) -> None:
        if self.updates:
            diff = self._time_diff(datetime.now(), self.updates[0].time)
            if diff > self.new_alert_time:
                self.updates.clear()

    @staticmethod
    def _time_diff(date1: datetime, date2: datetime) -> float:
        return abs((date1 - date2).total_seconds())

    @staticmethod
    def _parse_message(msg: str) -> tuple[list[int], int, datetime, bool]:
        pieces = msg.split(",")
        is_event = not bool(int(pieces[2]))
        cities = [int(c) for c in pieces[3].split("/")]
        region = int(pieces[4])
        date = datetime.strptime(pieces[5] + "," + pieces[6], "%Y/%m/%d,%H:%M:%S")
        return cities, region, date, is_event

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
        return f"Alert(time={alert.time.isoformat()}, " \
               f"states={alert.states}," \
               f" region={alert.region})"


class AlertDispatcher(AbstractService):
    """ Send alerts to other services such as FeedWriter and FeedPoster.
    """
    def __init__(self, alerts: queue.Queue):
        super().__init__()
        self._alerts = alerts
        self._to_write = queue.Queue()
        self._to_post = queue.Queue()
        self.wait = 0.1

    @property
    def to_write(self) -> queue.Queue:
        return self._to_write

    @property
    def to_post(self) -> queue.Queue:
        return self._to_post

    def _handle_event(self):
        while not self._stop:
            self._dispatch_alerts()

    def _dispatch_alerts(self) -> None:
        alert = self._get_from_queue(self._alerts, self.wait)
        if alert is not None:
            self.to_write.put(alert)
            self.to_post.put(copy.deepcopy(alert))


class FeedWriter(AbstractService):
    """ Receives Alert objects and writes a cap file. """

    def __init__(self, alerts: queue.Queue):
        super().__init__()
        self._alerts = alerts
        self.save_path = CONFIG.SAVE_PATH

        self.wait = 0.2
        self.alert_filename = CONFIG.ALERT_FILE_NAME
        self.update_filename = CONFIG.UPDATE_FILE_NAME
        self.event_filename = CONFIG.EVENT_FILE_NAME
        self.event_update_filename = CONFIG.EVENT_UPDATE_FILE_NAME

    @property
    def alerts(self) -> queue.Queue:
        return self._alerts

    def _handle_event(self):
        """ Get new Alerts and write a cap file.
        """
        while not self._stop:
            alert = self._get_from_queue(self._alerts, self.wait)
            if alert is not None:
                self._write_alert(alert)

    def _write_alert(self, alert: Alert) -> None:
        if alert is not None:
            filename = get_cap_file_name(alert)
            feed = create_feed(alert, is_test=False)

            feed_path = os.path.join(self.save_path, f"{filename}_{feed.updated_date}.cap")
            write_feed_to_file(feed_path, feed)

            logger.info(f"Cap file written to {feed_path}")


class FeedPoster(AbstractService):
    """ Class to post the cap feeds to our API so, they can be saved
        in the database.
    """
    def __init__(self, alerts: queue.Queue):
        super().__init__()
        self.wait = 0.1
        self._alerts = alerts
        self._client = APIClient()

    @property
    def client(self) -> APIClient:
        return self._client

    def _handle_event(self):
        while not self._stop:
            self._post_alerts()

    def _post_alerts(self):
        alert = self._get_from_queue(self._alerts, self.wait)
        if alert is not None:
            res = self._client.post_alert(alert)
            if res.ok:
                logger.info("Posted new alert to API")
            else:
                logger.info("Failed to post alert to API")

