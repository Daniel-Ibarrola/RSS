import os
from rss.logger import check_log_file


def test_creates_new_log_file_after_current_gets_big():
    file_name = "temp.log"
    logs_path = "./"
    with open(file_name, "w") as fp:
        fp.write("Hello World " * 5)

    size = 10  # in bytes
    check_log_file(logs_path, file_name, size)

    log_files = []
    for root, dirs, filenames in os.walk(logs_path):
        for file_ in filenames:
            if file_.endswith(".log"):
                log_files.append(file_)

    assert len(log_files) == 2
    with open(file_name) as fp:
        assert fp.readlines() == []

    for logfile in log_files:
        os.remove(logfile)
