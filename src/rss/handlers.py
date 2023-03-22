from datetime import datetime
import queue
import threading
import time
from typing import Optional

from rss.alert import Alert
from rss.rss import create_feed, write_feed_to_file

# TODO: get correct polygons
POLYGONS = {
    40: (1., 2., 3., 4., 5., 6., 7., 8., 9.,),
    41: (2., 3., 4., 5., 6., 7., 8., 9., 10.,),
    42: (11., 12., 13., 14., 15., 16., 17., 18., 19.,),
    43: (1., 2., 3., 4., 5., 6., 7., 8., 9.,),
    44: (1., 2., 3., 4., 5., 6., 7., 8., 9.,),
    45: (1., 2., 3., 4., 5., 6., 7., 8., 9.,),
    46: (1., 2., 3., 4., 5., 6., 7., 8., 9.,),
    47: (1., 2., 3., 4., 5., 6., 7., 8., 9.,),
    48: (1., 2., 3., 4., 5., 6., 7., 8., 9.,),
    49: (1., 2., 3., 4., 5., 6., 7., 8., 9.,),
}


class AlertHandler:

    def __init__(self, data_queue: queue.Queue, alerts: Optional[queue.Queue] = None):
        self.queue = data_queue  # type: queue.Queue[bytes]

        self._process_thread = threading.Thread(
            target=self._process_messages, daemon=True
        )
        self._stop = False
        self.new_alert_time = 60  # in seconds
        self._wait = 1
        # Initialize to alert with old date and fake city
        self._last_alert = Alert(
            time=datetime(2020, 1, 1), city=-1, region=41203, polygons=[], geocoords=(0, 0)
        )

        if alerts is None:
            self.alerts = queue.Queue()  # type: queue.Queue[Alert]
        else:
            self.alerts = alerts

    def _process_messages(self):
        while not self._stop:
            msg = self._get_message()
            if msg is not None:
                msg = msg.decode().strip()
                if msg.startswith("84,3"):
                    city, region, date = self._parse_message(msg)
                    time_diff = abs((self._last_alert.time - date).total_seconds())
                    if time_diff > self.new_alert_time:
                        # TODO: get geocoords
                        self._last_alert = Alert(
                            time=date, city=city, region=region,
                            polygons=[POLYGONS[city]], geocoords=(0, 0)
                        )
                        self.alerts.put(self._last_alert)
                    elif self._last_alert.city != city:
                        self._last_alert.polygons.append(POLYGONS[city])

            time.sleep(self._wait)

    def _get_message(self) -> bytes:
        try:
            return self.queue.get(timeout=1)
        except queue.Empty:
            pass

    @staticmethod
    def _parse_message(msg: str) -> tuple[int, int, datetime]:
        pieces = msg.split(",")
        city, region = int(pieces[2]), int(pieces[3])
        date = datetime.strptime(pieces[4] + "," + pieces[5], "%Y/%m/%d,%H:%M:%S")
        return city, region, date

    def run(self):
        self._process_thread.start()

    def join(self):
        self._process_thread.join()

    def shutdown(self):
        self._stop = True
        self.join()
