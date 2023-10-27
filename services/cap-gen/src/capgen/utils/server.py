import datetime
from socketlib import Server, send_msg
from socketlib.utils.logger import get_module_logger
import time

from rss import CONFIG


MESSAGES = [
        # Test 1: Skips unwanted messages
        ("15,3,3242,41203, ,46237.1234567890", 1),

        # Test 2: Alert with update
        ("84,3,1,41/42,41203, ,46237.1234567890", 2.),
        ("84,3,1,43,41203, ,46237.1234567890", 15.),

        # Test 4: Non-alert event
        ("84,3,0,44,41203, ,46237.1234567890", 30.),
    ]


class AlertServer(Server):
    """ Server for testing.

        Generates alert messages.
    """

    def _send(self) -> None:
        self._connected.wait()
        index = 0
        while not self._stop_send():
            msg, wait, index = self.get_message(index)
            msg = self.add_time_to_msg(msg)
            error = send_msg(
                self._connection, msg, logger=self._logger, name="AlertServer"
            )
            if not error and self._logger:
                self._logger.info(f"Msg sent {msg.strip()}")
            if error:
                break
            time.sleep(wait)

    @staticmethod
    def get_message(index) -> tuple[str, float, int]:
        if index >= len(MESSAGES):
            index = 0
        msg, wait = MESSAGES[index]
        index += 1
        return msg, wait, index

    @staticmethod
    def add_time_to_msg(msg: str) -> str:
        pieces = msg.split(",")
        now = datetime.datetime.now()
        new_msg = ",".join(pieces[:5])
        new_msg += "," + now.strftime("%Y/%m/%d,%H:%M:%S")
        new_msg += "," + ",".join(pieces[6:])
        return new_msg


def get_time() -> str:
    now = datetime.datetime.now()
    return now.strftime("%Y/%m/%d,%H:%M:%S")


def start_server() -> None:
    logger = get_module_logger("AlertServer", "dev", use_file_handler=False)
    server = AlertServer(
        address=(CONFIG.IP, CONFIG.PORT),
        reconnect=False,
        logger=logger
    )
    logger.info(f"AlertServer will listen in {(server.ip, server.port)}")

    with server:
        server.start()

        try:
            server.join()
        except KeyboardInterrupt:
            server.shutdown()

    logger.info("Graceful shutdown")


if __name__ == "__main__":
    start_server()
