import copy
import logging
import queue
from typing import Callable, Optional

from socketlib.basic.queues import get_from_queue
from socketlib.services import AbstractService

from rss.cap.alert import Alert


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