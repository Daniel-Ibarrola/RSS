from bs4 import BeautifulSoup
import os
import threading
from typing import Any

from rss import CONFIG
from rss.main import get_services, main
from server import get_server, start_server


def shutdown_services(server_shutdown: threading.Event, services: list[Any]):
    server_shutdown.wait()
    for serv in services:
        serv.shutdown()


def test_writes_cap_files_when_receiving_alerts():
    # The client is started and will listen for alerts of the server
    server = get_server(log=False)
    services = get_services()

    server_shutdown = threading.Event()
    server_thread = threading.Thread(target=start_server, args=(server, server_shutdown, False))
    services_thread = threading.Thread(target=main, args=services)
    shutdown_thread = threading.Thread(target=shutdown_services, args=(server_shutdown, services))

    shutdown_thread.start()
    server_thread.start()
    services_thread.start()

    server_thread.join()
    shutdown_thread.join()
    services_thread.join()

    # The client receives an alert with an update, and after a certain time an event
    # Three files should have been written. One for the alert, one for the update and
    # another for the event.
    files = []
    for root, _, filenames in os.walk(CONFIG.SAVE_PATH):
        for file in filenames:
            if file.endswith(".cap"):
                files.append(os.path.join(root, file))

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
    alert = data.feed.entry.alert
    assert alert.info.event.string == "Sismo"
    assert alert.info.severity.string == "Minor"
    assert len(alert.find_all("polygon")) == 1

    for file in files:
        os.remove(file)


if __name__ == "__main__":
    test_writes_cap_files_when_receiving_alerts()
