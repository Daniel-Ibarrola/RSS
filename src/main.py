import queue

from rss.client import TCPClient
from rss.handlers import AlertHandler
from rss.logger import get_module_logger

logger = get_module_logger(__name__)


def main():
    # TODO: arg parser
    # TODO: monitor threads
    # TODO: two clients
    ip, port = "localhost", 12345

    data_queue = queue.Queue()

    client = TCPClient(ip, port, data_queue, logging=True)
    client.msg_time = 5
    logger.info("Starting client")

    # alert_handler = AlertHandler(data_queue)

    with client:
        client.connect()
        client.run(daemon=True)
        # alert_handler.run()

        try:
            client.join()
            # alert_handler.join()
        except KeyboardInterrupt:
            client.shutdown()
            # alert_handler.shutdown()

    print("Client received the following messages:")
    while not client.queue.empty():
        print(client.queue.get().decode().strip())


if __name__ == "__main__":
    main()
