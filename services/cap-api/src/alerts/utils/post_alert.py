import datetime
from typing import Optional

from rss.cap.alert import Alert
from rss.cap.states import STATES_CODES

from alerts.client.api_client import APIClient
from alerts.utils.alert_id import alert_id


def get_references(
        client: APIClient, ref_ids: list[str], refs: list[Alert]
) -> None:
    for ref_id in ref_ids:
        res = client.get_alert_by_id(ref_id)
        if not res.ok:
            raise IOError(
                f"Failed to get alert reference with id {ref_id}. "
                f"Status code: {res.status_code}."
            )
        alert_json = res.json()
        if len(alert_json["references"] > 0):
            get_references(client, alert_json["references"], refs)
        refs.append(Alert.from_json(res.json()))


def post_alert(
        client: APIClient,
        date_str: str,
        states: list[str | int],
        region: int,
        is_event: bool,
        ref_ids: Optional[list[str]] = None
):
    """ Post a new alert to the API
    """
    date = datetime.datetime.fromisoformat(date_str)

    state_codes = [STATES_CODES[st] if isinstance(st, str) else st for st in states]

    if ref_ids:
        alert_refs = []
        get_references(client, ref_ids, alert_refs)
    else:
        alert_refs = None

    res = client.post_alert(Alert(
        time=date,
        states=state_codes,
        region=region,
        id=alert_id(date),
        is_event=is_event,
        refs=alert_refs
    ))
    print("Posted alert")
    print(f"Status code {res.status_code}")
    print(res.content)


if __name__ == "__main__":
    alerts = [
        {"date_str": "2024-01-30T19:01:06", "states": [43], "region": 43206},
        {"date_str": "2024-01-30T22:04:07", "states": [42], "region": 42208},
        {"date_str": "2024-01-31T01:25:33", "states": [41], "region": 41207},
        {"date_str": "2024-02-01T00:28:05", "states": [41], "region": 41201},
        {"date_str": "2024-02-02T10:14:12", "states": [44], "region": 44205},
        {"date_str": "2024-02-03T12:52:34", "states": [41], "region": 41207},
    ]
    client = APIClient(
        "https://rss.sasmex.net/",
    )
    for alert in alerts:
        post_alert(
            client,
            date_str=alert["date_str"],
            states=alert["states"],
            region=alert["region"],
            is_event=True
        )
