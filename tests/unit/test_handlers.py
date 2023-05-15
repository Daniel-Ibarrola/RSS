import datetime
import os
import pickle
import queue
import time

import pytest

import rss.handlers
from rss import handlers
from rss.alert import Alert


class TestAlertHandler:

    def test_parse_message(self):
        msg = "84,3,40,41203,2023/03/22,14:04:33,46237.1234567890"
        city, region, date = handlers.AlertHandler._parse_message(msg)
        assert city == 40
        assert region == 41203
        assert date == datetime.datetime(2023, 3, 22, 14, 4, 33)

    @staticmethod
    def put_in_queue(messages):
        data = queue.Queue()
        for msg in messages:
            data.put(msg)
        return data

    @staticmethod
    def queue_to_list(queue_: queue.Queue):
        data = []
        while not queue_.empty():
            data.append(queue_.get())
        return data

    def test_only_process_messages_with_correct_code(self):
        msg = b"15,3,40,41203,2023/03/22,14:04:33,46237.1234567890\r\n"
        alert_handler = handlers.AlertHandler(queue.Queue())
        alert = alert_handler._get_alert(msg)

        assert alert is None

    def test_check_city_not_in_queue(self):
        alert_handler = handlers.AlertHandler(queue.Queue())
        alert_handler.cities_queue.append((40, datetime.datetime(2023, 3, 22, 14, 4, 33)))
        assert alert_handler._check_city(42)

    def test_check_city_in_queue(self):
        alert_handler = handlers.AlertHandler(queue.Queue())
        alert_handler.cities_queue.append((40, datetime.datetime(2023, 3, 22, 14, 4, 33)))
        assert not alert_handler._check_city(40)

    def test_flush_cities_queue(self):
        alert_handler = handlers.AlertHandler(queue.Queue())
        alert_handler.new_alert_time = 60

        date1 = datetime.datetime.now() - datetime.timedelta(seconds=70)
        alert_handler.cities_queue.append((40, date1))
        alert_handler.cities_queue.append((44, date1))

        date2 = datetime.datetime.now()
        alert_handler.cities_queue.append((42, date2))

        alert_handler._flush_cities_queue()
        assert alert_handler.cities_queue == [(42, date2)]

    def test_msgs_of_same_city_are_ignored_if_arrive_before_time(self):
        msg1 = b"84,3,40,41203,2023/03/22,14:04:33,46237.1234567890\r\n"
        msg2 = b"84,3,40,41203,2023/03/22,14:04:34,46237.1234567890\r\n"
        alert_handler = handlers.AlertHandler(queue.Queue())
        alert_handler.new_alert_time = 5
        alert1 = alert_handler._get_alert(msg1)
        alert2 = alert_handler._get_alert(msg2)
        # Alerts of the same city arriving before new alert time are
        # considered equal
        assert alert1 == Alert(
            time=datetime.datetime(2023, 3, 22, 14, 4, 33),
            city=40,
            region=41203,
            polygons=[handlers.POLYGONS[40]],
        )
        assert alert2 is None

    def test_process_messages(self):
        date1 = datetime.datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
        data = self.put_in_queue([
            f"84,3,40,41203,{date1},46237.1234567890\r\n".encode("utf-8"),
            f"84,3,40,41203,{date1},46237.1234567890\r\n".encode("utf-8"),
            # Garbage data should be ignored
            f"15,3,40,41203,{date1},46237.1234567890\r\n".encode("utf-8"),
        ])
        alert_handler = handlers.AlertHandler(data)
        alert_handler.new_alert_time = 1
        alert_handler._wait = 0
        alert_handler.run()

        time.sleep(1)

        date2 = datetime.datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
        data.put(f"84,3,41,41203,{date2},46237.1234567890\r\n".encode("utf-8"))
        time.sleep(3)

        alert_handler.shutdown()

        assert len(alert_handler.cities_queue) == 0
        assert self.queue_to_list(alert_handler.alerts) == [
            Alert(time=datetime.datetime.strptime(date1, "%Y/%m/%d,%H:%M:%S"),
                  city=40,
                  region=41203,
                  polygons=[handlers.POLYGONS[40]],

                  ),
            Alert(time=datetime.datetime.strptime(date2, "%Y/%m/%d,%H:%M:%S"),
                  city=41,
                  region=41203,
                  polygons=[handlers.POLYGONS[41]],

                  ),
        ]


def clear_file():
    base_path = os.path.dirname(__file__)
    alert_path = os.path.join(base_path, "alert.pickle")
    if os.path.exists(alert_path):
        os.remove(alert_path)


@pytest.fixture
def clear_alert_file():
    clear_file()
    yield
    clear_file()


class TestFeedWriter:

    @pytest.mark.usefixtures("clear_alert_file")
    def test_load_last_alert_file_does_not_exist(self):
        base_path = os.path.dirname(__file__)
        assert rss.handlers.FeedWriter._load_last_alert(base_path) is None

    @pytest.mark.usefixtures("clear_alert_file")
    def test_load_last_alert(self):
        alert = Alert(
            time=datetime.datetime(2023, 3, 24),
            city=40,
            region=41203,
            polygons=[handlers.POLYGONS[40]],
        )

        base_path = os.path.dirname(__file__)
        alert_path = os.path.join(base_path, "alert.pickle")
        with open(alert_path, "wb") as fp:
            pickle.dump(alert, fp)

        alert_loaded = rss.handlers.FeedWriter._load_last_alert(base_path)
        assert alert == alert_loaded

    def test_check_last_alert_alerts_within_time_range(self):
        alert1 = Alert(
            time=datetime.datetime(2023, 3, 24, 1, 0, 0),
            city=40,
            region=41203,
            polygons=[handlers.POLYGONS[40]],
        )
        alert2 = Alert(
            time=datetime.datetime(2023, 3, 24, 1, 0, 2),
            city=40,
            region=41203,
            polygons=[handlers.POLYGONS[40]],
        )

        assert not rss.handlers.FeedWriter._check_last_alert(alert1, alert2)

    def test_check_last_alert_different_polygons(self):
        alert1 = Alert(
            time=datetime.datetime(2023, 3, 24, 1, 0, 0),
            city=40,
            region=41203,
            polygons=[handlers.POLYGONS[40]],
        )
        alert2 = Alert(
            time=datetime.datetime(2023, 3, 24, 1, 0, 2),
            city=40,
            region=41203,
            polygons=[handlers.POLYGONS[41]],
        )

        assert rss.handlers.FeedWriter._check_last_alert(alert1, alert2)

    def test_check_last_alert_alerts_out_of_time_range(self):
        alert1 = Alert(
            time=datetime.datetime(2023, 3, 24, 1, 0, 0),
            city=40,
            region=41203,
            polygons=[handlers.POLYGONS[40]],
        )
        alert2 = Alert(
            time=datetime.datetime(2023, 3, 24, 1, 0, 15),
            city=40,
            region=41203,
            polygons=[handlers.POLYGONS[40]],
        )

        assert rss.handlers.FeedWriter._check_last_alert(alert1, alert2)
