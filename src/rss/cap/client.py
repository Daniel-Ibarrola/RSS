import datetime
import dataclasses
import queue
import socket
import struct
import threading
import time

from rss import CONFIG
from rss.utils.logger import get_module_logger

logger = get_module_logger(__name__)


@dataclasses.dataclass(frozen=True)
class Disconnected:
    time: datetime.datetime


class TCPClient:

    def __init__(
            self, ip: str, port: int, data_queue: queue.Queue
    ):
        self._ip = ip
        self._port = port
        self._socket = None  # type: socket.socket

        self._send_thread, self._rcv_thread = self._get_threads()
        self._reconnect_thread = threading.Thread(target=self._reconnect, daemon=True)

        self._stop = False
        self._stop_reconnect = False

        self.queue = data_queue
        self.msg_time = CONFIG.MSG_TIME

        self.errors = queue.Queue()
        self.threads_dict = {}

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def port(self) -> int:
        return self._port

    @property
    def send_thread(self) -> threading.Thread:
        return self._send_thread

    @property
    def rcv_thread(self) -> threading.Thread:
        return self._rcv_thread

    @property
    def reconnect_thread(self) -> threading.Thread:
        return self._reconnect_thread

    def connect(self) -> None:
        """ Connect to the server. """
        while True:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self._socket.connect((self.ip, self.port))
                break
            except ConnectionError:
                time.sleep(2)

        logger.info(f"{self.__class__.__name__}: connected to {(self.ip, self.port)}")

    def set_timeout(self, timeout: float):
        """ Set a timeout for sending and receiving messages.
        """
        timeval = struct.pack("ll", timeout, 0)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, timeval)

    @staticmethod
    def encode_message(msg: str) -> bytes:
        """ Encode a message to be ready to be sent."""
        msg += "\r\n"
        return msg.encode("utf-8")

    def _get_threads(self):
        return (
            threading.Thread(target=self._send, daemon=True),
            threading.Thread(target=self._receive, daemon=True),
        )

    def _send(self):
        """ Send a recognition message to the server every 30 seconds.
        """
        msg = self.encode_message("Hello World")
        while not self._stop:
            try:
                self._socket.sendall(msg)
            except ConnectionError:
                self.errors.put(Disconnected(time=datetime.datetime.now()))
                break
            time.sleep(self.msg_time)

        logger.debug("Send thread stopped")

    def _receive(self):
        """ Receive data and put it in another server. """
        while not self._stop:
            try:
                data = self._socket.recv(2048)
                if data:
                    self.queue.put(data)
            except ConnectionError:
                break

        logger.debug("Receive thread stopped")

    def _reconnect(self):
        """ Reconnect to the server in case."""
        while not self._stop_reconnect:
            try:
                error = self.errors.get(timeout=1)
            except queue.Empty:
                time.sleep(2)
                continue

            logger.info(f"Client disconnected at {error.time}")
            self._stop = True
            self.join(reconnect=False)
            self.connect()

            self._send_thread, self._rcv_thread = self._get_threads()
            self.threads_dict["client_send"] = self._send_thread
            self.threads_dict["client_rcv"] = self._rcv_thread

            self.run(reconnect=False)

    def run(self, reconnect: bool = True) -> None:
        """ Start the sending and receiving threads. """
        self._stop = False
        self._stop_reconnect = False

        self._send_thread.start()
        self._rcv_thread.start()

        if reconnect:
            self._reconnect_thread.start()

    def shutdown(self) -> None:
        """ Stop all the threads. """
        self._stop = True
        self._stop_reconnect = True
        logger.info(f"{self.__class__.__name__}: stopping")

        self.join()
        logger.info(f"{self.__class__.__name__}: disconnected")

    def join(self, reconnect=True):
        self._rcv_thread.join()
        self._send_thread.join()
        if reconnect:
            self._reconnect_thread.join()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._socket is not None:
            self._socket.close()
