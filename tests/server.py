import datetime
import socket
import threading
import time


class ServerConnectionError(Exception):
    pass


class Server:

    def __init__(self, ip, port):
        self.port = port
        self.ip = ip
        self.socket = self.wait_to_connect(self.ip, self.port)
        self.connection = None

        self.stop = False
        self.rcv_thread = threading.Thread(target=self.receive, daemon=True)
        self.send_thread = threading.Thread(target=self.send, daemon=True)

        self.queue = []
        self.messages = [
            ("Hello World1\r\n", 5),
            ("Hello World2\r\n", 3),
        ]

    @staticmethod
    def connect(ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen()
        print(f"Server listening on {ip}:{port}")
        return sock

    def wait_to_connect(self, ip, port):
        start = time.time()

        while time.time() - start < 60:
            try:
                return self.connect(ip, port)
            except OSError:
                self.port += 1

        raise ServerConnectionError("Failed to start server")

    def receive(self):
        while not self.stop:
            try:
                msg = self.connection.recv(1024)
            except ConnectionError:
                break
            if msg:
                print(msg)
                self.queue.append(msg)

    def send(self):
        exit_ = False
        while not self.stop:
            for msg, wait_time in self.messages:
                msg = self._add_time_to_msg(msg)
                try:
                    self.connection.sendall(msg.encode("utf-8"))
                except ConnectionError:
                    exit_ = True
                    break
                time.sleep(wait_time)
            if exit_:
                break
            print("All messages have been sent. Repeating...")

    @staticmethod
    def _add_time_to_msg(msg: str) -> str:
        pieces = msg.split(",")
        new_msg = ",".join(pieces[:4]) + "," + get_time() + "," + ",".join(pieces[5:])
        return new_msg

    def run(self):
        self.connection, _ = self.socket.accept()
        print("Connection accepted")

        self.stop = False
        self.rcv_thread.start()
        self.send_thread.start()

    def join(self):
        self.send_thread.join()
        self.rcv_thread.join()

    def shutdown(self):
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


def start_server():
    print("TCP Server")
    server = Server("localhost", 12345)
    server.n_messages = 30

    server.messages = [
        # Test 1: Skips unwanted messages
        ("84,3,40,41203, ,46237.1234567890\r\n", 2),
        ("15,3,40,41203, ,46237.1234567890\r\n", 5),

        # Test 2: Writes all polygons
        ("84,3,40,41203, ,46237.1234567890\r\n", 0),
        ("84,3,41,41203, ,46237.123456f789f0\r\n", 0),
        ("84,3,42,41203, ,46237.1234567890\r\n", 5),

        # Test 3: Different alerts
        ("84,3,40,41203, ,46237.1234567890\r\n", 5),
        ("84,3,40,41203, ,46237.1234567890\r\n", 10),

        # Test 4: Small earthquake code
        ("84,2,40,41203, ,46237.1234567890\r\n", 5),
    ]

    with server:
        server.run()
        try:
            server.join()
        except KeyboardInterrupt:
            server.shutdown()

    print("Server received the following messages:")
    print(server.queue)


if __name__ == "__main__":
    start_server()
