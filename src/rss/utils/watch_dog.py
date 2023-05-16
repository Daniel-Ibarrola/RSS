import threading
import time
import os

from rss.utils.logger import get_module_logger

logger = get_module_logger(__name__)


class WatchDog:
    """ Verifies that all threads are running.
    """
    def __init__(self, threads: dict[str, threading.Thread] = None):
        if threads is None:
            self.threads = {}  # type: dict[str, threading.Thread]
        else:
            self.threads = threads

        self.check_thread = threading.Thread(target=self.check_threads, daemon=True)
        self.wait = 5
        self._stop = False

        self.n_attempts = 0
        self.tolerance = 4

    def check_threads(self):
        exit_ = False
        while not self._stop:
            for thread_name, thread in self.threads.items():
                if not thread.is_alive():

                    # receive and send threads may be dead if reconnecting. So we'll give only exit
                    # after some time has passed
                    if thread_name == "client_send" or thread_name == "client_rcv":
                        if self.n_attempts < self.tolerance:
                            self.n_attempts += 1
                            continue

                    logger.info(f"Thread {thread_name} is dead")
                    exit_ = True

            if exit_:
                break

            time.sleep(self.wait)

        if exit_:
            logger.info("Some threads are dead. Exiting...")
            time.sleep(2)
            # Exit application
            os._exit(1)

    def run(self):
        self.check_thread.start()

    def join(self):
        self.check_thread.join()

    def shutdown(self):
        self._stop = True
        self.join()
