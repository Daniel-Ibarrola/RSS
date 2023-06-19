import dataclasses
import datetime


@dataclasses.dataclass(frozen=True)
class Alert:
    time: datetime.datetime
    states: list[int]
    region: int
    id: str = ""
    is_event: bool = False
    refs: list["Alert"] = None
