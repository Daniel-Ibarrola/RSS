import time
import datetime
import os
import pytest
import queue
import random
import threading

from bs4 import BeautifulSoup
import requests
from socketlib import Server
from socketlib.utils.logger import get_module_logger

from capgen import CONFIG
from capgen.main import main
from capgen.services.api_client import APIClient


class TestCAPGenerator:

    address = "localhost", random.randint(1024, 49150)
    api_url = os.environ.get("API_URL", "")

    @staticmethod
    def get_cap_files() -> list[str]:
        files = []
        for root, _, filenames in os.walk(CONFIG.SAVE_PATH):
            for file in filenames:
                if file.endswith(".cap") and "test" in file:
                    files.append(os.path.join(root, file))
        return files

    @staticmethod
    def remove_files(files: list[str]) -> None:
        for file in files:
            os.remove(file)

    @pytest.fixture
    def server(self) -> Server:
        """ Server sends alert messages to client.
            Also expects to receive alive messages from client.

            Yields
            ------
            Server
        """
        logger = get_module_logger("Server", "dev", use_file_handler=False)
        received = queue.Queue()
        to_send = queue.Queue()

        date1 = datetime.datetime.now()
        date2 = date1 + datetime.timedelta(minutes=5)
        date1_str = date1.strftime('%Y/%m/%d,%H:%M:%S')
        date2_str = date2.strftime('%Y/%m/%d,%H:%M:%S')
        # Test 1: Skips unwanted messages
        to_send.put(f"15,3,3242,41203,{date1_str},46237.1234567890")
        # Test 2: Alert with update
        to_send.put(f"84,3,1,41/42,41203,{date1_str},46237.1234567890")
        to_send.put(f"84,3,1,43,41203,{date1_str},46237.1234567890")
        # Test 3: Non-alert event
        to_send.put(f"84,3,0,44,41203,{date2_str},46237.1234567890")

        stop = threading.Event()
        server_ = Server(
            address=self.address,
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

        stop.set()
        server_.join()
        server_.close_connection()

    @pytest.fixture
    def cleanup_files(self):
        files = self.get_cap_files()
        self.remove_files(files)
        yield
        files = self.get_cap_files()
        self.remove_files(files)

    @pytest.fixture
    def wait_for_api(self):
        """ If the API_URL env variable set, this fixture will
            try to connect to send a request to the API, if it fails
            it will retry for 10 seconds.
        """
        start = time.time()
        if self.api_url:
            while time.time() - start < 10:
                try:
                    requests.get(self.api_url)
                    return
                except requests.ConnectionError:
                    continue
            pytest.fail("Could not connect to API")

    @pytest.mark.timeout(10)
    @pytest.mark.usefixtures("wait_for_api")
    def test_saves_cap_feeds_when_receiving_alerts(self, server, cleanup_files):
        # The client is started and will listen for alerts of the server
        logger = get_module_logger("Main", "dev", use_file_handler=False)
        stop_event = threading.Event()
        thread = threading.Thread(
            target=main,
            kwargs=dict(
                address=self.address,
                reconnect=False,
                timeout=2,
                heart_beats=0.5,
                api_url=self.api_url,
                use_watchdog=False,
                stop=lambda: stop_event.is_set(),
                logger=logger,
                exit_error=False
            )
        )
        thread.start()
        time.sleep(3)  # Give the services some time to process all data

        logger.info("Waiting for services to end")
        stop_event.set()
        thread.join()

        # The client receives an alert with an update, and after a certain time an event
        # Three files should have been written. One for the alert, one for the update and
        # another for the event.
        files = self.get_cap_files()
        assert len(files) == 3

        logger.info(f"Found files {files}")

        [alert] = [f for f in files if "alert" in f]
        [update] = [f for f in files if "update" in f]
        [event] = [f for f in files if "event" in f]

        with open(alert) as fp:
            data = BeautifulSoup(fp.read(), "xml")

        # We check the first alert, which was triggered in two cities
        # so, it should have two polygons
        alert = data.feed.entry.alert
        assert "SASMEX: ALERTA SISMICA" in alert.info.event.string
        assert alert.info.severity.string == "Severe"
        assert len(alert.find_all("polygon")) == 2

        identifier = alert.identifier.string

        with open(update) as fp:
            data = BeautifulSoup(fp.read(), "xml")

        # We check the update alert. It should reference the previous alert
        alert = data.feed.entry.alert
        references = alert.references.string
        assert "SASMEX: ALERTA SISMICA" in alert.info.event.string
        assert alert.info.severity.string == "Severe"

        # The update should contain the previous polygon as well as the new one
        assert len(alert.find_all("polygon")) == 3
        assert identifier in references

        with open(event) as fp:
            data = BeautifulSoup(fp.read(), "xml")

        # Finally, we check the event
        event = data.feed.entry.alert
        assert "SASMEX: Sismo Moderado" in event.info.event.string
        assert event.info.severity.string == "Unknown"
        assert len(event.find_all("circle")) == 1

        self.remove_files(files)

        if self.api_url:
            # Now we check that the feeds have been stored in the database
            client = APIClient(self.api_url)
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
