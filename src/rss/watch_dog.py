import threading
import time
import sys

from rss.logger import get_module_logger

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

    def check_threads(self):
        exit_ = False
        while not self._stop:
            for thread_name, thread in self.threads.items():
                if not thread.is_alive():
                    logger.info(f"Thread {thread_name} is dead")
                    exit_ = True

            if exit_:
                break

            time.sleep(self.wait)

        if exit_:
            logger.info("Some threads are dead. Exiting...")
            sys.exit(1)

    def run(self):
        self.check_thread.start()

    def join(self):
        self.check_thread.join()

    def shutdown(self):
        self._stop = True
        self.join()
