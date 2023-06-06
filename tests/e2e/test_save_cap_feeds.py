from bs4 import BeautifulSoup
import os
import pytest
import threading
from typing import Any

from rss import CONFIG
from rss.main import get_services, main
from rss.api.client import APIClient
from server import get_server, start_server


def shutdown_services(server_shutdown: threading.Event, services: list[Any]):
    watch_dog = services.pop()
    server_shutdown.wait()
    watch_dog.shutdown()
    for serv in services:
        serv.shutdown()


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


@pytest.fixture
def cleanup_files():
    files = get_cap_files()
    remove_files(files)
    yield
    files = get_cap_files()
    remove_files(files)


@pytest.mark.usefixtures("postgres_session")
@pytest.mark.usefixtures("wait_for_api")
def test_saves_cap_feeds_when_receiving_alerts(cleanup_files):
    # The client is started and will listen for alerts of the server
    server = get_server(log=False)
    services = get_services()

    server_shutdown = threading.Event()
    server_thread = threading.Thread(target=start_server, args=(server, server_shutdown, False))
    services_thread = threading.Thread(target=main, args=(services, ))
    shutdown_thread = threading.Thread(target=shutdown_services, args=(server_shutdown, list(services)))

    shutdown_thread.start()
    server_thread.start()
    services_thread.start()

    server_thread.join()
    shutdown_thread.join()
    services_thread.join()

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

    # We check the first alert
    alert = data.feed.entry.alert
    assert alert.info.event.string == "Alerta por sismo"
    assert alert.info.severity.string == "Severe"
    assert len(alert.find_all("polygon")) == 1

    identifier = alert.identifier.string

    with open(update) as fp:
        data = BeautifulSoup(fp.read(), "xml")

    # We check the update alert. It should reference the previous alert
    alert = data.feed.entry.alert
    references = alert.references.string
    assert alert.info.event.string == "Alerta por sismo"
    assert alert.info.severity.string == "Severe"

    # The update should contain the previous polygon as well as the new one
    assert len(alert.find_all("polygon")) == 2
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
    assert alert["city"] == 41
    assert len(alert["references"]) == 0
    assert not alert["is_event"]

    update = json["alerts"][1]
    assert update["city"] == 43
    assert len(update["references"]) == 1
    assert not update["is_event"]

    event = json["alerts"][0]
    assert event["city"] == 44
    assert len(event["references"]) == 0
    assert event["is_event"]


if __name__ == "__main__":
    test_saves_cap_feeds_when_receiving_alerts(None)
