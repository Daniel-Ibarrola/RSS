import time

from bs4 import BeautifulSoup
import datetime
import os
import pytest
import queue
import random
from socketlib import Server
from socketlib.utils.logger import get_module_logger
import threading

from rss import CONFIG
from rss.main import main
from rss.services.api_client import APIClient


def get_cap_files() -> list[str]:
    files = []
    for root, _, filenames in os.walk(CONFIG.SAVE_PATH):
        for file in filenames:
            if file.endswith(".cap") and "test" in file:
                files.append(os.path.join(root, file))
    return files


def remove_files(files: list[str]) -> None:
    for file in files:
        os.remove(file)


address = "localhost", random.randint(1024, 49150)


@pytest.fixture
def server() -> Server:
    """ Server sends alert messages to client.
        Also expects to receive alive messages from client.

        Yields
        ------
        Server
    """
    logger = get_module_logger("Server", "dev", use_file_handler=False)
    received = queue.Queue()
    to_send = queue.Queue()

    now = datetime.datetime.now()
    now_str = now.strftime("%Y/%m/%d,%H:%M:%S")
    # Test 1: Skips unwanted messages
    to_send.put(f"15,3,3242,41203,{now_str},46237.1234567890")
    # Test 2: Alert with update
    to_send.put(f"84,3,1,41/42,41203,{now_str},46237.1234567890")
    to_send.put(f"84,3,1,43,41203,{now_str},46237.1234567890")
    # Test 3: Non-alert event
    to_send.put(f"84,3,0,44,41203,{now_str},46237.1234567890")

    server_ = Server(
        address=address,
        received=received,
        to_send=to_send,
        reconnect=False,
        timeout=2,
        stop_receive=lambda: received.qsize() >= 1,
        stop_send=lambda: to_send.empty(),
        logger=logger
    )
    server_.start()

    yield server_

    try:
        server_.shutdown()
    finally:
        server_.close_connection()


@pytest.fixture
def cleanup_files():
    files = get_cap_files()
    remove_files(files)
    yield
    files = get_cap_files()
    remove_files(files)


@pytest.mark.timeout(10)
@pytest.mark.usefixtures("postgres_session")
@pytest.mark.usefixtures("wait_for_api")
def test_saves_cap_feeds_when_receiving_alerts(server, cleanup_files):
    # The client is started and will listen for alerts of the server
    logger = get_module_logger("Main", "dev", use_file_handler=False)
    stop_event = threading.Event()
    thread = threading.Thread(
        target=main,
        kwargs=dict(
            address=address,
            reconnect=False,
            timeout=2,
            heart_beats=0.5,
            use_watchdog=False,
            stop=lambda: stop_event.is_set(),
            logger=logger,
            exit_error=False
        )
    )
    thread.start()
    time.sleep(1)  # Give the services some time to process all data

    logger.info("Waiting for services to end")
    stop_event.set()
    thread.join()

    # The client receives an alert with an update, and after a certain time an event
    # Three files should have been written. One for the alert, one for the update and
    # another for the event.
    files = get_cap_files()
    assert len(files) == 3

    [alert] = [f for f in files if "alert" in f]
    [update] = [f for f in files if "update" in f]
    [event] = [f for f in files if "event" in f]

    with open(alert) as fp:
        data = BeautifulSoup(fp.read(), "xml")

    # We check the first alert, which was triggered in two cities
    # so, it should have two polygons
    alert = data.feed.entry.alert
    assert alert.info.event.string == "Alerta por sismo"
    assert alert.info.severity.string == "Severe"
    assert len(alert.find_all("polygon")) == 2

    identifier = alert.identifier.string

    with open(update) as fp:
        data = BeautifulSoup(fp.read(), "xml")

    # We check the update alert. It should reference the previous alert
    alert = data.feed.entry.alert
    references = alert.references.string
    assert alert.info.event.string == "Alerta por sismo"
    assert alert.info.severity.string == "Severe"

    # The update should contain the previous polygon as well as the new one
    assert len(alert.find_all("polygon")) == 3
    assert identifier in references

    with open(event) as fp:
        data = BeautifulSoup(fp.read(), "xml")

    # Finally, we check the event
    event = data.feed.entry.alert
    assert event.info.event.string == "Sismo"
    assert event.info.severity.string == "Minor"
    assert len(event.find_all("circle")) == 1

    remove_files(files)

    # Now we check that the feeds have been stored in the database
    client = APIClient()
    res = client.get_alerts()
    assert res.ok

    json = res.json()
    assert len(json["alerts"]) == 3

    alert = json["alerts"][2]
    assert alert["states"] == [41, 42]
    assert len(alert["references"]) == 0
    assert not alert["is_event"]

    update = json["alerts"][1]
    assert update["states"] == [43]
    assert len(update["references"]) == 1
    assert not update["is_event"]

    event = json["alerts"][0]
    assert event["states"] == [44]
    assert len(event["references"]) == 0
    assert event["is_event"]


if __name__ == "__main__":
    test_saves_cap_feeds_when_receiving_alerts(None)
