import datetime

from rss.api.client import APIClient
from rss.cap.alert import Alert


def main():
    client = APIClient()
    client.base_url = "https://mapa.sasmex.net/api/v1"
    alert = Alert(
        time=datetime.datetime(2023, 4, 3, 20, 12, 18),
        city=40,
        region=42207,
        id="2023419105959",
        is_event=False,
    )

    res = client.post_alert(alert, save_file=True)
    print(res.status_code)
    print(res.content)


if __name__ == "__main__":
    main()
