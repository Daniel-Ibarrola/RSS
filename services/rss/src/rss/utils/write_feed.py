import datetime
from typing import Literal
from rss.cap.alert import Alert
from rss.cap.rss import create_feed, write_feed_to_file
from rss.cap.states import STATES_CODES


def write_cap_file(
        date_str: str,
        states: list[str],
        region: int,
        alert_type: Literal["alert", "event", "test"],
        save_path: str
):
    date = datetime.datetime.fromisoformat(date_str)
    state_codes = [STATES_CODES[st] for st in states]
    is_event = True if alert_type == "event" else False
    is_test = True if alert_type == "test" else False

    alert = Alert(
        time=date,
        states=state_codes,
        region=region,
        id="TEST_ID",
        is_event=is_event,
    )
    feed = create_feed(alert, is_test=is_test)
    write_feed_to_file(save_path, feed)
    print(f"CAP file written to {save_path}")


if __name__ == "__main__":
    write_cap_file(
        datetime.datetime.now().isoformat(),
        ["CDMX"],
        41201,
        "alert",
        "../../../feeds/test.xml"
    )
