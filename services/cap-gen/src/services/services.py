import copy
from datetime import datetime
import logging
import os
import queue
import random
import string
from typing import Callable, Optional, Union

import requests
from socketlib.basic.queues import get_from_queue
from socketlib.services import AbstractService

from rss import CONFIG
from rss.services.api_client import APIClient
from rss.cap.alert import Alert
from rss.cap.rss import create_feed, write_feed_to_file, get_cap_file_name


class MessageProcessor(AbstractService):
    """ Receives alert messages and if they are valid, converts them to an
        Alert object that can be used to create cap feeds.

        Alert msg format:

        84,3,Event/Alert,City1/City2/.../CityN,Station,yyyy/mm/dd,hh:mm:ss,hourMsg\r\n

        Where

        Event/Alert = 0 for events. 1 for alerts
        hourMsg = unix time the message was sent
    """

    def __init__(self,
                 messages: Optional[queue.Queue[bytes]] = None,
                 alerts: Optional[queue.Queue] = None,
                 stop: Optional[Callable[[], bool]] = None,
                 logger: Optional[logging.Logger] = None
                 ):
        super().__init__(
            in_queue=messages,
            out_queue=alerts,
            stop=stop,
            logger=logger
        )
        self._updates = []  # type: list[Alert]
        self.new_alert_time = CONFIG.ALERT_TIME  # in seconds
        self.wait = 0.1

    @property
    def updates(self) -> list[Alert]:
        return self._updates

    @property
    def messages(self) -> queue.Queue[bytes]:
        return self._in

    @property
    def alerts(self) -> queue.Queue[Alert]:
        return self._out

    def _handle_message(self) -> None:
        """ Get new messages and create or update alerts.
        """
        while not self._stop():
            msg = get_from_queue(self.messages, 1)
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

            self._flush_updates(date)
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
                if self._logger:
                    self._logger.info(f"New alert: {self._alert_str(alert)}")
                return alert

    def _check_state(self, state: int) -> bool:
        """ Checks that the given state is not in the queue"""
        return not any(s == state for alert in self.updates for s in alert.states)

    def _flush_updates(self, new_alert_date: datetime) -> None:
        if self.updates:
            diff = self._time_diff(new_alert_date, self.updates[0].time)
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
        refs = [] if alert.refs is None else alert.refs
        return f"Alert(time={alert.time.isoformat()}, " \
               f"states={alert.states}," \
               f"region={alert.region}) " \
               f"refs={[a.id for a in refs]})"


class AlertDispatcher(AbstractService):
    """ Send alerts to other services such as FeedWriter and FeedPoster.
    """
    def __init__(
            self,
            alerts: Optional[queue.Queue[Alert]] = None,
            stop: Optional[Callable[[], bool]] = None,
            logger: Optional[logging.Logger] = None
    ):
        super().__init__(
            in_queue=alerts,
            stop=stop,
            logger=logger
        )
        self._to_write = queue.Queue()
        self._to_post = queue.Queue()
        self.wait = 0.1

    @property
    def to_write(self) -> queue.Queue[Alert]:
        return self._to_write

    @property
    def to_post(self) -> queue.Queue[Alert]:
        return self._to_post

    @property
    def alerts(self) -> queue.Queue[Alert]:
        return self._in

    def _handle_message(self):
        while not self._stop():
            self._dispatch_alerts()

    def _dispatch_alerts(self) -> None:
        alert = get_from_queue(self.alerts, self.wait)
        if alert is not None:
            self.to_write.put(alert)
            self.to_post.put(copy.deepcopy(alert))


class FeedWriter(AbstractService):
    """ Receives Alert objects and writes a cap file. """

    def __init__(
            self,
            alerts: Optional[queue.Queue[Alert]] = None,
            stop: Optional[Callable[[], bool]] = None,
            logger: Optional[logging.Logger] = None
    ):
        super().__init__(
            in_queue=alerts,
            stop=stop,
            logger=logger
        )
        self.save_path = CONFIG.SAVE_PATH
        self.wait = 0.2

    @property
    def alerts(self) -> queue.Queue[Alert]:
        return self._in

    def _handle_message(self):
        """ Get new Alerts and write a cap file.
        """
        while not self._stop():
            alert = get_from_queue(self.alerts, self.wait)
            if alert is not None:
                self._write_alert(alert)

    def _write_alert(self, alert: Alert) -> None:
        if alert is not None:
            filename = get_cap_file_name(alert)
            feed = create_feed(alert, is_test=False)

            feed_path = os.path.join(self.save_path, f"{filename}_{feed.updated_date}.cap")
            write_feed_to_file(feed_path, feed)

            if self._logger:
                self._logger.info(f"Cap file written to {feed_path}")


class FeedPoster(AbstractService):
    """ Class to post the cap feeds to our API so, they can be saved
        in the database.
    """
    def __init__(
            self,
            alerts: Optional[queue.Queue[Alert]] = None,
            api_url: str = CONFIG.API_URL,
            stop: Optional[Callable[[], bool]] = None,
            logger: Optional[logging.Logger] = None
    ):
        super().__init__(
            in_queue=alerts,
            stop=stop,
            logger=logger
        )
        self.wait = 0.1
        self._client = APIClient(api_url)

    @property
    def client(self) -> APIClient:
        return self._client

    @property
    def alerts(self) -> queue.Queue[Alert]:
        return self._in

    def _handle_message(self):
        while not self._stop():
            self._post_alerts()

    def _post_alerts(self):
        alert = get_from_queue(self.alerts, self.wait)
        if alert is not None:
            try:
                res = self.client.post_alert(alert, CONFIG.POST_API_PATH)
            except requests.ConnectionError:
                if self._logger:
                    self._logger.info(
                        f"Post alert connection error. "
                        f"Failed to post alert to {self.client.base_url}")
                return

            if res.ok and self._logger:
                self._logger.info("Posted new alert to API")
            elif self._logger:
                self._logger.info(
                    f"Failed to post alert to API "
                    f"Status code: {res.status_code}")
