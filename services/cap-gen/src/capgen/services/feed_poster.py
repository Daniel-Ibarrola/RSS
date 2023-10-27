import logging
import queue
from typing import Callable, Optional

import requests
from rss.cap.alert import Alert
from socketlib.basic.queues import get_from_queue
from socketlib.services import AbstractService

from capgen import CONFIG
from capgen.services.api_client import APIClient


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
