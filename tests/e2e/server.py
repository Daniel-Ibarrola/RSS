import datetime
import socket
import threading
import time


class ServerConnectionError(Exception):
    pass


class Server:
    """ Fake server for testing.

        Generates fake messages simulating alerts.
    """

    def __init__(self, ip: str, port: int, log: bool = True):
        self.port = port
        self.ip = ip
        self.socket = self.wait_to_connect(self.ip, self.port)
        self.connection = None

        self.stop = False
        self.rcv_thread = threading.Thread(target=self.receive, daemon=True)
        self.send_thread = threading.Thread(target=self.send, daemon=True)
        self.log = log

        self.queue = []
        self.messages = [
            ("Hello World1\r\n", 5),
            ("Hello World2\r\n", 3),
        ]

    @staticmethod
    def connect(ip: str, port: int) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen()
        print(f"Server listening on {ip}:{port}")
        return sock

    def wait_to_connect(self, ip: str, port: int) -> socket.socket:
        start = time.time()

        while time.time() - start < 60:
            try:
                return self.connect(ip, port)
            except OSError:
                self.port += 1

        raise ServerConnectionError("Failed to start server")

    def receive(self) -> None:
        while not self.stop:
            try:
                msg = self.connection.recv(1024)
            except ConnectionError:
                break
            if msg:
                if self.log:
                    print(msg)
                self.queue.append(msg)

    def send(self) -> None:
        for msg, wait_time in self.messages:
            msg = self._add_time_to_msg(msg)
            try:
                self.connection.sendall(msg.encode("utf-8"))
            except ConnectionError:
                break

            time.sleep(wait_time)
        self.stop = True
        if self.log:
            print("All messages have been sent. Exiting...")

    def accept(self) -> None:
        self.connection, _ = self.socket.accept()
        if self.log:
            print("Connection accepted")

    @staticmethod
    def _add_time_to_msg(msg: str) -> str:
        pieces = msg.split(",")
        new_msg = ",".join(pieces[:4]) + "," + get_time() + "," + ",".join(pieces[5:])
        return new_msg

    def run(self) -> None:
        th = threading.Thread(target=self.accept, daemon=True)
        th.start()
        th.join()

        self.stop = False
        self.rcv_thread.start()
        self.send_thread.start()

    def join(self):
        self.send_thread.join()
        self.rcv_thread.join()

    def shutdown(self):
        if self.log:
            print("Shutting down")
        self.stop = True
        self.join()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.connection is not None:
            self.connection.close()
        self.socket.close()


def get_time() -> str:
    now = datetime.datetime.now()
    return now.strftime("%Y/%m/%d,%H:%M:%S")


def get_server(log: bool = True) -> Server:
    print("TCP Server")
    server = Server("localhost", 12345, log=log)

    server.messages = [
        # Test 1: Skips unwanted messages
        ("15,3,3242,41203, ,46237.1234567890\r\n", 2),

        # Test 2: Alert with update
        ("84,3,41,41203, ,46237.1234567890\r\n", 0),
        ("84,3,43,41203, ,46237.1234567890\r\n", 5),

        # Test 4: Non-alert event
        ("84,2,44,41203, ,46237.1234567890\r\n", 5),
    ]

    return server


def start_server(server: Server,
                 server_shutdown: threading.Event,
                 log: bool) -> None:
    with server:
        server.run()
        try:
            server.join()
        except KeyboardInterrupt:
            server.shutdown()

    server_shutdown.set()
    if log:
        print("Server received the following messages:")
        print(server.queue)

    # TODO: automate google cap validator test


if __name__ == "__main__":
    start_server(get_server())
