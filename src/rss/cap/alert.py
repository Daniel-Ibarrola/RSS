import dataclasses
import datetime
from typing import Any, Optional


@dataclasses.dataclass(frozen=True)
class Alert:
    time: datetime.datetime
    states: list[int]
    region: int
    id: str = ""
    is_event: bool = False
    refs: Optional[list["Alert"]] = None

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> "Alert":
        """ Create an alert from a dictionary. If the dictionary
            has references to other alerts, they are not considered.
        """
        return cls(
            time=datetime.datetime.fromisoformat(json["time"]),
            states=json["states"],
            region=json["region"],
            is_event=json["is_event"],
            id=json["id"],
        )
