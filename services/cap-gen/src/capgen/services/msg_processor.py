import copy
from datetime import datetime
import logging
import queue
import random
import string
from typing import Callable, Optional, Union

from rss.cap.alert import Alert
from socketlib.basic.queues import get_from_queue
from socketlib.services import AbstractService

from capgen import CONFIG


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