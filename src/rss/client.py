import socket
import struct
import threading
import time
import queue


class TCPClient:

    def __init__(
            self, ip: str, port: int, logging: bool = True
    ):
        self._ip = ip
        self._port = port
        self._socket = None  # type: socket.socket
        self._logging = logging
        self._stop = False

        self._send_thread = None
        self._rcv_thread = None
        self.queue = queue.Queue()
        self.msg_time = 30

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def port(self) -> int:
        return self._port

    def connect(self) -> None:
        """ Connect to the server. """
        while True:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self._socket.connect((self.ip, self.port))
                break
            except ConnectionError:
                time.sleep(2)

        self._log(f"{self.__class__.__name__}: connected to {(self.ip, self.port)}")

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

    def _log(self, msg: str):
        if self._logging:
            print(msg)

    def _send(self):
        """ Send a recognition message to the server every 30 seconds.
        """
        msg = self.encode_message("Hello World")
        while not self._stop:
            try:
                self._socket.sendall(msg)
            except ConnectionError:
                break
            time.sleep(self.msg_time)

    def _receive(self):
        """ Receive data and put it in another server. """
        while not self._stop:
            try:
                data = self._socket.recv(2048)
                if data:
                    self.queue.put(data)
            except ConnectionError:
                break

    def run(self, daemon: bool) -> None:
        """ Start the sending and receiving threads. """
        self._send_thread = threading.Thread(target=self._send, daemon=daemon)
        self._rcv_thread = threading.Thread(target=self._receive, daemon=daemon)
        self._send_thread.start()
        self._rcv_thread.start()

    def shutdown(self) -> None:
        """ Stop all the threads. """
        self._stop = True
        self._log(f"{self.__class__.__name__}: stopping")

        self.join()
        self._log(f"{self.__class__.__name__}: disconnected")

    def join(self):
        self._rcv_thread.join()
        self._send_thread.join()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._socket is not None:
            self._socket.close()
