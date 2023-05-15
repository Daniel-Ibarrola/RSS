import time
import pytest

from rss.client import TCPClient


# TODO: fix tests

@pytest.mark.skip(reason="Tests hang")
def test_client_sends_and_receives_from_server():
    ip, port = "localhost", 12345
    server = Server(ip, port)
    server.n_messages = 2

    client = TCPClient(ip, port, logging=False)
    client.msg_time = 1

    server.run()
    client.run(daemon=True)

    time.sleep(3)
    server.shutdown()
    client.shutdown()

    assert client.queue.get() == b"msg 1\r\n"
    assert client.queue.get() == b"msg 2\r\n"
    assert client.queue.empty()

    assert b"Hello World\r\n" in server.queue


@pytest.mark.skip(reason="Tests hang")
def test_client_waits_for_server_if_server_is_not_serving():
    ip, port = "localhost", 12345
    client = TCPClient(ip, port, logging=False)
    client.run(daemon=True)

    time.sleep(2)

    server = Server(ip, port)
    server.n_messages = 1
    server.run()
    time.sleep(1)

    server.shutdown()
    client.shutdown()

    assert client.queue.get() == b"msg 1\r\n"
    assert client.queue.empty()


@pytest.mark.skip(reason="Tests hang")
def test_client_reconnects():
    ip, port = "localhost", 12345
    server = Server(ip, port)
    server.n_messages = 1
    client = TCPClient(ip, port, logging=False)

    server.run()
    client.run(daemon=True)

    server.shutdown()
    time.sleep(2)

    server = Server(ip, port)
    server.n_messages = 1
    server.run()

    assert client.queue.get() == b"msg 1\r\n"
    assert client.queue.get() == b"msg 1\r\n"
    assert client.queue.empty()
    