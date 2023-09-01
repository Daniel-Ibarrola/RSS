import threading
from socketlib import Client
from socketlib.utils.watch_dog import WatchDog
from socketlib.utils.logger import get_module_logger

from rss import CONFIG
from rss.services import services

logger = get_module_logger(__name__,
                           "dev",
                           use_file_handler=False)


def get_threads_dict(client: Client,
                     message_processor: services.MessageProcessor,
                     dispatcher: services.AlertDispatcher,
                     writer: services.FeedWriter,
                     poster: services.FeedPoster) -> dict[str, threading.Thread]:
    return {
        "client_send": client.send_thread,
        "client_rcv": client.receive_thread,
        "message_processor": message_processor.process_thread,
        "dispatcher": dispatcher.process_thread,
        "feed_writer": writer.process_thread,
        "feed_poster": poster.process_thread,
    }


def get_services() -> tuple[
        Client,
        services.MessageProcessor,
        services.AlertDispatcher,
        services.FeedWriter,
        services.FeedPoster,
        WatchDog,
]:
    address = CONFIG.IP, CONFIG.PORT

    client = Client(address)
    logger.info(f"Client will attempt to connect to {address}")

    message_processor = services.MessageProcessor(client.received)
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
        Client,
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
        client.start()
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
