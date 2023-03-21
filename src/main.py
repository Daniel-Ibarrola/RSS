from rss.client import TCPClient
from rss.logger import get_module_logger

logger = get_module_logger(__name__)


def main():
    ip, port = "localhost", 12345
    client = TCPClient(ip, port, logging=True)
    client.msg_time = 5
    logger.info("Starting client")

    with client:
        client.connect()
        client.run(daemon=True)

        try:
            client.join()
        except KeyboardInterrupt:
            client.shutdown()

    print("Client received the following messages:")
    while not client.queue.empty():
        print(client.queue.get().decode().strip())


if __name__ == "__main__":
    main()
