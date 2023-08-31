import datetime
import os
import sys

from rss.api.client import APIClient
from rss.cap.alert import Alert


def main():
    client = APIClient()
    # client.base_url = "https://mapa.sasmex.net/api/v1"

    rss_type = "alert"
    if len(sys.argv) > 1:
        rss_type = sys.argv[1]
        if rss_type not in ["alert", "event", "update"]:
            raise ValueError(f"Incorrect type {rss_type}")

    save_path = ""
    if len(sys.argv) > 2:
        save_path = sys.argv[2]
        if "localhost" in client.base_url and not os.path.isdir(save_path):
            raise ValueError(f"Incorrect path {save_path}")

    alert = Alert(
        time=datetime.datetime.now(),
        states=[40, 48],
        region=41204,
        id="2023419105959",
        is_event=False,
    )
    event = Alert(
        time=datetime.datetime.now(),
        states=[40],
        region=41204,
        id="2023419105959",
        is_event=True,
    )
    update = Alert(
        time=datetime.datetime.now(),
        states=[47],
        region=41204,
        id="3123419105959",
        is_event=False,
        refs=[alert]
    )

    if rss_type == "alert":
        res = client.post_alert(alert, save_path)
    elif rss_type == "update":
        res = client.post_alert(update, save_path)
    elif rss_type == "event":
        res = client.post_alert(event, save_path)
    else:
        raise ValueError(f"Incorrect type {rss_type}")

    print(res.status_code)
    print(res.content)


if __name__ == "__main__":
    main()
