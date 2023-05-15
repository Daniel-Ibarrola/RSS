import dataclasses
import datetime

from rss.data import GeoPoint, Polygon


@dataclasses.dataclass(frozen=True)
class Alert:
    time: datetime.datetime
    city: int
    region: int
    polygons: list[Polygon]
    triggered: bool = True
