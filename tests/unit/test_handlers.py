import datetime
import queue
import time

from rss.cap import handlers
from rss.cap.alert import Alert


class TestAlertHandler:

    def test_parse_message(self):
        msg = "84,3,40,41203,2023/03/22,14:04:33,46237.1234567890"
        city, region, date = handlers.AlertHandler._parse_message(msg)
        assert city == 40
        assert region == 41203
        assert date == datetime.datetime(2023, 3, 22, 14, 4, 33)

    @staticmethod
    def compare_alerts(alert1: Alert, alert2: Alert) -> bool:
        """ Compare two alerts but ignore their ids. """
        time_diff = (alert1.time - alert2.time).total_seconds()

        return (time_diff < 1
                and alert1.refs == alert2.refs
                and alert1.city == alert2.city
                and alert1.region == alert2.region
                and alert1.is_event == alert2.is_event
                )

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
        alert = Alert(
            time=datetime.datetime(2023, 3, 24),
            city=40,
            region=41203,
        )
        alert_handler.updates.append(alert)
        assert alert_handler._check_city(42)

    def test_check_city_in_queue(self):
        alert_handler = handlers.AlertHandler(queue.Queue())
        alert = Alert(
            time=datetime.datetime(2023, 3, 24),
            city=40,
            region=41203,
        )
        alert_handler.updates.append(alert)
        assert not alert_handler._check_city(40)

    def test_flush_updates_queue(self):
        alert_handler = handlers.AlertHandler(queue.Queue())
        alert_handler.new_alert_time = 60

        date1 = datetime.datetime.now() - datetime.timedelta(seconds=70)
        alert1 = Alert(
            time=date1,
            city=40,
            region=41203,
        )
        alert2 = Alert(
            time=date1,
            city=44,
            region=41203,
        )
        alert_handler.updates.append(alert1)
        alert_handler.updates.append(alert2)
        alert_handler._flush_updates()
        assert len(alert_handler.updates) == 0

    def test_msgs_of_same_city_are_ignored_if_arrive_before_time(self):
        date1 = datetime.datetime.now() - datetime.timedelta(seconds=30)
        date2 = datetime.datetime.now() - datetime.timedelta(seconds=25)

        date1_str = date1.strftime("%Y/%m/%d,%H:%M:%S")
        date2_str = date2.strftime("%Y/%m/%d,%H:%M:%S")

        msg1 = f"84,3,40,41203,{date1_str},46237.1234567890\r\n"
        msg2 = f"84,3,40,41203,{date2_str},46237.1234567890\r\n"

        alert_handler = handlers.AlertHandler(queue.Queue())
        alert_handler.new_alert_time = 60

        alert1 = alert_handler._get_alert(msg1.encode("utf-8"))
        alert_handler.updates.append(alert1)

        alert2 = alert_handler._get_alert(msg2.encode("utf-8"))
        # Alerts of the same city arriving before new alert time are
        # considered equal
        assert self.compare_alerts(alert1, Alert(
            time=date1,
            city=40,
            region=41203,
        ))
        assert alert2 is None

    def test_creates_new_alerts_after_alert_time(self):
        date1 = datetime.datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
        data = self.put_in_queue([
            f"84,3,40,41203,{date1},46237.1234567890\r\n".encode("utf-8"),
            f"84,3,40,41203,{date1},46237.1234567890\r\n".encode("utf-8"),
            # Garbage data should be ignored
            f"15,3,40,41203,{date1},46237.1234567890\r\n".encode("utf-8"),
        ])
        alert_handler = handlers.AlertHandler(data)
        alert_handler.new_alert_time = 0.75
        alert_handler.wait = 0
        alert_handler.run()

        time.sleep(1.5)

        date2 = datetime.datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
        data.put(f"84,3,41,41203,{date2},46237.1234567890\r\n".encode("utf-8"))
        time.sleep(1)

        alert_handler.shutdown()

        alerts = self.queue_to_list(alert_handler.alerts)
        # The last alert should be stored as an update
        assert len(alert_handler.updates) == 1
        assert alert_handler.updates[0].city == 41
        assert len(alerts) == 2

        first_alert = alerts[0]
        assert first_alert.refs is None  # Means is not an update
        assert first_alert.time == datetime.datetime.strptime(date1, "%Y/%m/%d,%H:%M:%S")
        assert first_alert.city == 40
        assert first_alert.region == 41203

        second_alert = alerts[1]
        assert second_alert.refs is None  # Means is not an update
        assert second_alert.time == datetime.datetime.strptime(date2, "%Y/%m/%d,%H:%M:%S")
        assert second_alert.city == 41
        assert second_alert.region == 41203

    def test_updates_alerts_if_new_arrives_before_alert_time(self):
        date1 = datetime.datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
        data = self.put_in_queue([
            f"84,3,40,41203,{date1},46237.1234567890\r\n".encode("utf-8"),
        ])
        alert_handler = handlers.AlertHandler(data)
        alert_handler.new_alert_time = 5
        alert_handler._wait = 0
        alert_handler.run()

        time.sleep(1)

        date2 = datetime.datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
        data.put(f"84,3,41,41203,{date2},46237.1234567890\r\n".encode("utf-8"))
        time.sleep(2)

        alert_handler.shutdown()

        alerts = self.queue_to_list(alert_handler.alerts)
        assert len(alerts) == 2

        first_alert = alerts[0]
        alert_id = first_alert.id
        assert first_alert.refs is None  # Means is not an update
        assert first_alert.time == datetime.datetime.strptime(date1, "%Y/%m/%d,%H:%M:%S")
        assert first_alert.city == 40
        assert first_alert.region == 41203

        second_alert = alerts[1]
        references = alerts[1].refs
        assert len(references) == 1  # Means is an update
        assert references[0].id == alert_id

        assert second_alert.time == datetime.datetime.strptime(date2, "%Y/%m/%d,%H:%M:%S")
        assert second_alert.city == 41
        assert second_alert.region == 41203