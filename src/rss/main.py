import logging
from socketlib.utils.watch_dog import WatchDog
from socketlib.utils.logger import get_module_logger
import sys
from typing import Callable, Optional

from rss import CONFIG
from rss.services import (
    AlertsClient,
    AlertDispatcher,
    MessageProcessor,
    FeedWriter,
    FeedPoster
)


def main(
        address: tuple[str, int],
        reconnect: bool = False,
        timeout: Optional[float] = None,
        heart_beats: float = 30.,
        use_watchdog: bool = False,
        stop: Optional[Callable[[], bool]] = None,
        logger: Optional[logging.Logger] = None,
        exit_error: bool = True
) -> None:
    if logger is not None:
        logger.info(f"RSS CAP generator")
        logger.info(f"AlertsClient will attempt to connect to {address}")

    client = AlertsClient(
        address=address,
        reconnect=reconnect,
        heartbeats=heart_beats,
        timeout=timeout,
        logger=logger,
        stop_receive=stop,
        stop_send=stop
    )

    message_processor = MessageProcessor(client.received, stop=stop, logger=logger)
    alert_dispatcher = AlertDispatcher(message_processor.alerts, stop=stop, logger=logger)
    feed_writer = FeedWriter(alert_dispatcher.to_write, stop=stop, logger=logger)
    feed_poster = FeedPoster(alert_dispatcher.to_post, stop=stop, logger=logger)

    watchdog = None
    if use_watchdog:
        threads = {
            "client_send": client.send_thread,
            "client_rcv": client.receive_thread,
            "message_processor": message_processor.process_thread,
            "dispatcher": alert_dispatcher.process_thread,
            "feed_writer": feed_writer.process_thread,
            "feed_poster": feed_poster.process_thread,
        }
        watchdog = WatchDog(threads)

    error = True
    with client:
        client.connect()
        client.start()
        message_processor.start()
        alert_dispatcher.start()
        feed_writer.start()
        feed_poster.start()

        if watchdog:
            watchdog.start()

        try:
            if watchdog:
                watchdog.join()
            else:
                client.join()
        except KeyboardInterrupt:
            if logger:
                logger.info("Shutting down...")
            error = False

            if watchdog:
                watchdog.shutdown()
        finally:
            client.shutdown()
            alert_dispatcher.shutdown()
            feed_writer.shutdown()
            feed_poster.shutdown()

    if error and exit_error:
        if logger:
            logger.info("An error occurred, exiting...")
        sys.exit(1)

    logger.info("Graceful shutdown")


if __name__ == "__main__":
    main(
        address=(CONFIG.IP, CONFIG.PORT),
        timeout=None,
        heart_beats=CONFIG.MSG_TIME,
        use_watchdog=True,
        logger=get_module_logger(
            __name__, CONFIG.NAME, use_file_handler=False
        )
    )
