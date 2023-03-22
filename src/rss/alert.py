import dataclasses
import datetime


@dataclasses.dataclass(frozen=True)
class Alert:
    time: datetime.datetime
    city: int
    region: int
    polygons: list[tuple]
    geocoords: tuple[float, float]

