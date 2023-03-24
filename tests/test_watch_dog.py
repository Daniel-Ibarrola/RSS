import threading
import time
from rss import watch_dog


def test_calls_exit_when_a_thread_dies(mocker):

    def function_that_raises_error():
        while True:
            time.sleep(2)
            raise ValueError

    mock_exit = mocker.patch("rss.watch_dog.sys.exit")
    thread = threading.Thread(target=function_that_raises_error, daemon=True)

    dog = watch_dog.WatchDog()
    dog.threads["function"] = thread
    dog.wait = 0

    thread.start()
    dog.run()
    dog.join()

    mock_exit.assert_called_once()
