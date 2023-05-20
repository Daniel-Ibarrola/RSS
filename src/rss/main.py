import queue
import threading

from rss import CONFIG
from rss.cap.client import TCPClient
from rss.cap.services import MessageProcessor, FeedWriter
from rss.utils.logger import get_module_logger
from rss.utils.watch_dog import WatchDog

logger = get_module_logger(__name__)


def get_threads_dict(client: TCPClient,
                     alert_handler: MessageProcessor,
                     writer: FeedWriter) -> dict[str, threading.Thread]:
    return {
        "client_send": client.send_thread,
        "client_rcv": client.rcv_thread,
        "reconnect": client.reconnect_thread,
        "alert_handler": alert_handler.process_thread,
        "feed_writer": writer.process_thread,
    }


def get_services() -> tuple[WatchDog, TCPClient, MessageProcessor, FeedWriter]:
    ip, port = CONFIG.IP, CONFIG.PORT

    data_queue = queue.Queue()

    client = TCPClient(ip, port, data_queue)
    logger.info("Starting client")

    alert_handler = MessageProcessor(data_queue)
    feed_writer = FeedWriter(alert_handler.alerts)

    threads = get_threads_dict(client, alert_handler, feed_writer)
    watch_dog = WatchDog(threads)

    client.threads_dict = threads

    return watch_dog, client, alert_handler, feed_writer


def main(
    watch_dog: WatchDog,
    client: TCPClient,
    alert_handler: MessageProcessor,
    feed_writer: FeedWriter,
) -> None:

    with client:
        client.connect()
        client.run()
        alert_handler.run()
        feed_writer.run()
        watch_dog.run()

        try:
            watch_dog.join()
            client.join()
            alert_handler.join()
            feed_writer.join()
        except KeyboardInterrupt:
            watch_dog.shutdown()
            client.shutdown()
            alert_handler.shutdown()
            feed_writer.shutdown()

    logger.info("Graceful shutdown")


if __name__ == "__main__":
    main(*get_services())
