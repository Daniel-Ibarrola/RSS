import time
from collections import deque
import os
import queue
from rss.handlers import AlertHandler, FeedWriter


def main():
    msg_queue = deque([
        # Test 1: Skips unwanted messages
        b"84,3,40,41203,2023/03/22,14:04:00,46237.1234567890\r\n",
        b"15,3,40,41203,2023/03/22,14:04:00,46237.1234567890\r\n",

        # Test 2: Writes all polygons. 3 seconds later
        b"84,3,40,41203,2023/03/22,14:04:03,46237.1234567890\r\n",
        b"84,3,41,41203,2023/03/22,14:04:03,46237.123456f789f0\r\n",
        b"84,3,42,41203,2023/03/22,14:04:03,46237.1234567890\r\n",

        # Test 3: Different alerts
        b"84,3,40,41203,2023/03/22,14:04:07,46237.1234567890\r\n",
        b"15,3,40,41203,2023/03/22,14:04:12,46237.1234567890\r\n",
    ])

    data_queue = queue.Queue()
    alert_handler = AlertHandler(data_queue)
    alert_handler.new_alert_time = 2

    alert_handler.run()
    # Test 1
    data_queue.put(msg_queue.popleft())
    data_queue.put(msg_queue.popleft())
    time.sleep(2)
    # Test 2
    data_queue.put(msg_queue.popleft())
    data_queue.put(msg_queue.popleft())
    data_queue.put(msg_queue.popleft())
    time.sleep(2)
    # Test 3
    data_queue.put(msg_queue.popleft())
    data_queue.put(msg_queue.popleft())
    time.sleep(1)

    alert_handler.shutdown()


if __name__ == "__main__":
    main()
