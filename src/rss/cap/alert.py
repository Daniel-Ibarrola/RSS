import dataclasses
import datetime


@dataclasses.dataclass(frozen=True)
class Alert:
    time: datetime.datetime
    city: int
    region: int
    id: str = ""
    is_event: bool = False
    refs: list["Alert"] = None
