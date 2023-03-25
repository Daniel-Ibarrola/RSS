import os

import pytest

from rss.logger import check_log_file


def get_log_files(logs_path: str) -> list[str]:
    log_files = []
    for root, dirs, filenames in os.walk(logs_path):
        for file_ in filenames:
            if file_.endswith(".log"):
                log_files.append(file_)
    return log_files


@pytest.fixture
def clear_logs():
    yield
    log_files = get_log_files(os.path.dirname(__file__))
    for logfile in log_files:
        os.remove(logfile)


@pytest.mark.usefixture("clear_logs")
def test_creates_new_log_file_after_current_gets_big():
    logs_path = os.path.dirname(__file__)
    file_name = "temp.log"
    with open(os.path.join(logs_path, file_name), "w") as fp:
        fp.write("Hello World " * 5)

    size = 10  # in bytes
    check_log_file(logs_path, file_name, size)

    log_files = get_log_files(logs_path)
    assert len(log_files) == 2

    with open(os.path.join(logs_path, file_name)) as fp:
        assert fp.readlines() == []
