import dataclasses
import datetime

from rss.data import Polygon


# TODO: get geocoords

@dataclasses.dataclass(frozen=True)
class Alert:
    time: datetime.datetime
    city: int
    region: int
    polygons: list[Polygon]
    geocoords: tuple[float, float]
