from collections import defaultdict
import datetime
from typing import Optional

from rss.services.api_client import APIClient
from rss.cap.alert import Alert
from rss.cap.states import STATES
from rss.cap.regions import REGIONS


def region_codes_map() -> dict[str, set[int]]:
    """ Returns a map of the region name to region codes.

        A region can have multiple codes
    """
    region_codes = defaultdict(set)
    for code, region in REGIONS.items():
        region_codes[region].add(code)
    return region_codes


STATE_CODES = {name: code for code, name in STATES.items()}
REGION_CODES = region_codes_map()


class AlertFetchError(ValueError):
    pass


def get_references(
        client: APIClient, ref_ids: list[str], refs: list[Alert]
) -> None:
    for ref_id in ref_ids:
        res = client.get_alert_by_id(ref_id)
        if not res.ok:
            raise AlertFetchError(
                f"Failed to get alert reference with id {ref_id}. "
                f"Status code: {res.status_code}."
            )
        alert_json = res.json()
        if len(alert_json["references"] > 0):
            get_references(client, alert_json["references"], refs)
        refs.append(Alert.from_json(res.json()))


def post_alert(
        url: str,
        date_str: str,
        states: list[str],
        region: str,
        alert_id: str,
        is_event: bool,
        ref_ids: Optional[list[str]] = None
):
    """ Post a new alert to the API
    """
    client = APIClient(url)
    date = datetime.datetime.fromisoformat(date_str)
    state_codes = [STATE_CODES[st] for st in states]
    region_code = list(REGION_CODES[region])[0]

    if ref_ids:
        alert_refs = []
        get_references(client, ref_ids, alert_refs)
    else:
        alert_refs = None

    alert = Alert(
        time=date,
        states=state_codes,
        region=region_code,
        id=alert_id,
        is_event=is_event,
        refs=alert_refs
    )
    res = client.post_alert(alert)
    print(res.status_code)
    print(res.content)
