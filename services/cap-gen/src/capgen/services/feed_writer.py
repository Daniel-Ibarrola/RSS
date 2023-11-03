import logging
import os
import queue
from typing import Callable, Optional

from rss.cap.alert import Alert
from rss.cap.rss import create_feed, write_feed_to_file
from socketlib.basic.queues import get_from_queue
from socketlib.services import AbstractService

from capgen import CONFIG


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


def get_cap_file_name(alert: Alert) -> str:
    if alert.is_event and alert.refs is not None:
        return CONFIG.EVENT_UPDATE_FILE_NAME
    elif alert.is_event and alert.refs is None:
        return CONFIG.EVENT_FILE_NAME
    elif not alert.is_event and alert.refs is not None:
        return CONFIG.UPDATE_FILE_NAME
    else:
        return CONFIG.ALERT_FILE_NAME
