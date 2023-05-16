import dataclasses
import datetime

from rss.cap.data import Polygon


@dataclasses.dataclass(frozen=True)
class Alert:
    time: datetime.datetime
    city: int
    region: int
    polygons: list[Polygon]
    id: str = ""
    is_event: bool = False
