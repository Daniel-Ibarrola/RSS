import queue

from rss.client import TCPClient
from rss.handlers import AlertHandler, FeedWriter
from rss.logger import get_module_logger

logger = get_module_logger(__name__)


def main():
    # TODO: monitor threads
    # TODO: two clients
    ip, port = "localhost", 12345

    data_queue = queue.Queue()

    client = TCPClient(ip, port, data_queue, logging=True)
    logger.info("Starting client")

    alert_handler = AlertHandler(data_queue)
    feed_writer = FeedWriter(alert_handler.alerts)

    with client:
        client.connect()
        client.run()
        alert_handler.run()
        feed_writer.run()

        try:
            client.join()
            alert_handler.join()
            feed_writer.join()
        except KeyboardInterrupt:
            client.shutdown()
            alert_handler.shutdown()
            feed_writer.shutdown()

    logger.info("Graceful shutdown")


if __name__ == "__main__":
    main()
