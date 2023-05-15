import threading
import time
from rss import watch_dog


def function_that_raises_error():
    while True:
        time.sleep(2)
        raise ValueError


def test_calls_exit_when_a_thread_dies(mocker):
    mock_exit = mocker.patch("rss.watch_dog.os._exit")
    thread = threading.Thread(target=function_that_raises_error, daemon=True)

    dog = watch_dog.WatchDog()
    dog.threads["function"] = thread
    dog.wait = 0

    thread.start()
    dog.run()
    dog.join()

    mock_exit.assert_called_once()


def test_receive_and_send_threads_do_not_exit_on_first_time(mocker):
    mock_exit = mocker.patch("rss.watch_dog.os._exit")
    thread = threading.Thread(target=function_that_raises_error, daemon=True)

    dog = watch_dog.WatchDog()
    dog.threads["client_send"] = thread
    dog.tolerance = 2
    dog.wait = 1

    thread.start()
    dog.run()

    time.sleep(2)
    assert dog.check_thread.is_alive()
    dog.join()

    assert dog.n_attempts == 2
    mock_exit.assert_called_once()
