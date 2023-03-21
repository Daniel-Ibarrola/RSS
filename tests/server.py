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
        self.n_messages = 5
        self.queue = []

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
        for ii in range(self.n_messages):
            message = f"msg {ii + 1}\r\n".encode("utf-8")
            try:
                self.connection.sendall(message)
            except ConnectionError:
                break
            time.sleep(2)

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


def start_server():
    print("TCP Server")
    server = Server("localhost", 12345)
    server.n_messages = 30

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
