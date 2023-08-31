import queue
import threading

from rss import CONFIG
from rss.cap import services
from rss.cap.client import TCPClient
from rss.utils.logger import get_module_logger
from rss.utils.watch_dog import WatchDog

logger = get_module_logger(__name__,
                           use_file_handler=False)


def get_threads_dict(client: TCPClient,
                     message_processor: services.MessageProcessor,
                     dispatcher: services.AlertDispatcher,
                     writer: services.FeedWriter,
                     poster: services.FeedPoster) -> dict[str, threading.Thread]:
    return {
        "client_send": client.send_thread,
        "client_rcv": client.rcv_thread,
        "reconnect": client.reconnect_thread,
        "message_processor": message_processor.process_thread,
        "dispatcher": dispatcher.process_thread,
        "feed_writer": writer.process_thread,
        "feed_poster": poster.process_thread,
    }


def get_services() -> tuple[
        TCPClient,
        services.MessageProcessor,
        services.AlertDispatcher,
        services.FeedWriter,
        services.FeedPoster,
        WatchDog,
]:
    ip, port = CONFIG.IP, CONFIG.PORT

    data_queue = queue.Queue()

    client = TCPClient(ip, port, data_queue)
    logger.info("Starting client")

    message_processor = services.MessageProcessor(data_queue)
    alert_dispatcher = services.AlertDispatcher(message_processor.alerts)
    feed_writer = services.FeedWriter(alert_dispatcher.to_write)
    feed_poster = services.FeedPoster(alert_dispatcher.to_post)

    threads = get_threads_dict(
        client, message_processor, alert_dispatcher, feed_writer, feed_poster
    )
    watch_dog = WatchDog(threads)

    client.threads_dict = threads

    return (
        client,
        message_processor,
        alert_dispatcher,
        feed_writer,
        feed_poster,
        watch_dog,
    )


def main(processes: tuple[
        TCPClient,
        services.MessageProcessor,
        services.AlertDispatcher,
        services.FeedWriter,
        services.FeedPoster,
        WatchDog,
]) -> None:

    client = processes[0]
    watch_dog = processes[-1]
    service_list = list(processes[1:-1])

    with client:
        client.connect()
        client.run()
        for service in service_list:
            service.run()
        watch_dog.run()

        try:
            # Join the watch dog
            watch_dog.join()
        except KeyboardInterrupt:
            watch_dog.shutdown()
            client.shutdown()
            for service in service_list:
                service.shutdown()

    logger.info("Graceful shutdown")


if __name__ == "__main__":
    main(get_services())
