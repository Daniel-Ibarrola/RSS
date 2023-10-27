import logging
import time
from socketlib import Client
from socketlib.basic.send import send_msg
from typing import Callable, Optional


class AlertsClient(Client):
    """ Client that receives the alerts from new earthquakes and
        sends an alive message to the server every certain time.
    """
    def __init__(
            self,
            address: tuple[str, int],
            reconnect: bool = True,
            heartbeats: float = 30.,
            timeout: Optional[float] = None,
            stop_receive: Callable[[], bool] = None,
            stop_send: Callable[[], bool] = None,
            logger: Optional[logging.Logger] = None,
    ):
        super().__init__(
            address=address,
            reconnect=reconnect,
            timeout=timeout,
            stop_receive=stop_receive,
            stop_send=stop_send,
            logger=logger
        )
        self.heartbeats = heartbeats

    def _send_alive_message(self):
        while not self._stop_send():
            msg = "ALIVE"
            error = send_msg(
                self._socket, msg, self.msg_end,
                self._logger, self.__class__.__name__)
            if error:
                break
            time.sleep(self.heartbeats)

    def _send(self) -> None:
        """ Send an alive message to the server every certain time"""
        self._wait_for_connection.wait()
        if self._reconnect:
            while not self._stop_reconnect():
                self._send_alive_message()
                self._wait_for_connection.clear()
                self._connect_to_server(self._connect_timeout)
        else:
            self._send_alive_message()
