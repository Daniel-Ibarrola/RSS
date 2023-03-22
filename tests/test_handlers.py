import datetime
import queue
import time

from rss import handlers
from rss.alert import Alert
from rss.rss import RSSFeed


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
        data = self.put_in_queue([
            b"84,3,40,41203,2023/03/22,14:04:33,46237.1234567890\r\n"
            b"15,3,40,41203,2023/03/22,14:04:33,46237.1234567890\r\n"
        ])

        alert_handler = handlers.AlertHandler(data)
        alert_handler.new_alert_time = 0.5
        alert_handler._wait = 0
        alert_handler.run()
        time.sleep(1)
        alert_handler.shutdown()

        assert self.queue_to_list(alert_handler.alerts) == [
            Alert(time=datetime.datetime(2023, 3, 22, 14, 4, 33),
                  city=40,
                  region=41203,
                  polygons=[handlers.POLYGONS[40]],
                  geocoords=(0, 0)
                  )
        ]

    def test_msgs_of_same_city_are_ignored_if_arrive_before_time(self):
        data = self.put_in_queue([
            b"84,3,40,41203,2023/03/22,14:04:33,46237.1234567890\r"
            b"84,3,40,41203,2023/03/22,14:04:34,46237.1234567890\n"
        ])
        alert_handler = handlers.AlertHandler(data)
        # Alerts of the same city arriving before new alert time are
        # considered equal
        alert_handler.new_alert_time = 2
        alert_handler._wait = 0
        alert_handler.run()
        time.sleep(3)
        alert_handler.shutdown()

        assert self.queue_to_list(alert_handler.alerts) == [
            Alert(time=datetime.datetime(2023, 3, 22, 14, 4, 33),
                  city=40,
                  region=41203,
                  polygons=[handlers.POLYGONS[40]],
                  geocoords=(0, 0)
                  )
        ]

    def test_alert_contains_polygons_from_all_the_required_cities(self):
        data = self.put_in_queue([
            b"84,3,40,41203,2023/03/22,14:04:33,46237.1234567890\r"
            b"84,3,41,41203,2023/03/22,14:04:33,46237.1234567890\n"
            b"84,3,42,41203,2023/03/22,14:04:33,46237.1234567890\n"
        ])
        alert_handler = handlers.AlertHandler(data)
        # Alerts of the same city arriving before new alert time are
        # considered equal
        alert_handler.new_alert_time = 10
        alert_handler._wait = 0
        alert_handler.run()
        time.sleep(3)
        alert_handler.shutdown()

        assert self.queue_to_list(alert_handler.alerts) == [
            Alert(time=datetime.datetime(2023, 3, 22, 14, 4, 33),
                  city=40,
                  region=41203,
                  polygons=[handlers.POLYGONS[40],
                            handlers.POLYGONS[41],
                            handlers.POLYGONS[42]],
                  geocoords=(0, 0)
                  )
        ]

    def test_creates_new_alert_after_alert_time_passes(self):
        data = self.put_in_queue([
            b"84,3,40,41203,2023/03/22,14:04:33,46237.1234567890\r"
            b"84,3,40,41203,2023/03/22,14:04:35,46237.1234567890\n"
        ])
        alert_handler = handlers.AlertHandler(data)
        # Alerts of the same city arriving before new alert time are
        # considered equal
        alert_handler.new_alert_time = 1
        alert_handler.run()
        alert_handler._wait = 0
        time.sleep(3)
        alert_handler.shutdown()

        assert self.queue_to_list(alert_handler.alerts) == [
            Alert(time=datetime.datetime(2023, 3, 22, 14, 4, 33),
                  city=40,
                  region=41203,
                  polygons=[handlers.POLYGONS[40]],
                  geocoords=(0, 0)
                  ),
            Alert(time=datetime.datetime(2023, 3, 22, 14, 4, 35),
                  city=40,
                  region=41203,
                  polygons=[handlers.POLYGONS[40]],
                  geocoords=(0, 0)
                  ),
        ]


class TestFeedWriter:

    def test_creates_feeds(self, mocker):
        mock = mocker.patch(
            "rss.handlers.write_feed_to_file"
        )
        alert = Alert(
            time=datetime.datetime(2023, 3, 22, 14, 4, 33),
            city=40,
            region=41203,
            polygons=[handlers.POLYGONS[40]],
            geocoords=(0, 0)
        )
        alerts = queue.Queue()
        alerts.put(alert)

        feed_writer = handlers.FeedWriter(alerts)
        feed_writer.save_path = "/data"
        time.sleep(1)
        feed_writer.stop()

        mock.assert_called_once()
        call_args = mocker.call(
            "/data", RSSFeed(alert)
        )
