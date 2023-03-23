import datetime
import queue
import os
import pprint
import time

from rss.handlers import AlertHandler, FeedWriter


def put_in_queue(queue_: queue.Queue, items: list):
    for item in items:
        queue_.put(item)


def get_feed_writer(alerts):
    feed_writer = FeedWriter(alerts=alerts)
    base_path = os.path.dirname(__file__)
    feed_writer.save_path = os.path.abspath(os.path.join(base_path, "..", "feeds/"))
    feed_writer.wait = 0
    feed_writer.filename = "test"
    return feed_writer


def main():
    data_queue = queue.Queue()
    alert_handler = AlertHandler(data_queue)
    alert_handler.new_alert_time = 2
    alert_handler.wait = 0

    feed_writer = get_feed_writer(alert_handler.alerts)

    alert_handler.run()
    feed_writer.run()

    # Test 1: Skips unwanted messages
    date = datetime.datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
    msg1 = f"84,3,40,41203,{date},46237.1234567890\r\n".encode("utf-8")
    msg2 = f"15,3,40,41203,{date},14:04:00,46237.1234567890\r\n".encode("utf-8")
    put_in_queue(data_queue, [msg1, msg2])
    time.sleep(3)

    # Test 2: Writes all polygons. 3 seconds later
    date = datetime.datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
    msg1 = f"84,3,40,41203,{date},46237.1234567890\r\n".encode("utf-8")
    msg2 = f"84,3,41,41203,{date},46237.123456f789f0\r\n".encode("utf-8")
    msg3 = f"84,3,42,41203,{date},46237.1234567890\r\n".encode("utf-8")
    put_in_queue(data_queue, [msg1, msg2, msg3])
    time.sleep(3)

    # Test 3: Different alerts
    date = datetime.datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
    msg1 = f"84,3,40,41203,{date},46237.1234567890\r\n".encode("utf-8")
    put_in_queue(data_queue, [msg1])
    time.sleep(3)

    date = datetime.datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
    msg2 = f"84,3,40,41203,{date},46237.1234567890\r\n".encode("utf-8")
    put_in_queue(data_queue, [msg2])
    time.sleep(2)

    alert_handler.shutdown()
    feed_writer.shutdown()

    print("Alerts:")
    while not alert_handler.alerts.empty():
        pprint.pprint(alert_handler.alerts.get())


if __name__ == "__main__":
    main()
