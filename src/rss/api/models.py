import datetime
import logging
import os
from typing import Any, List, Literal, Optional
from sqlalchemy import func

from rss.api import db
from rss.cap.alert import Alert as CapAlert
from rss.cap.rss import create_feed
from rss.cap.regions import REGION_CODES


class Alert(db.Model):
    __tablename__ = "alerts"
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    time: db.Mapped[datetime.datetime] = db.mapped_column(db.TIMESTAMP, nullable=False)
    region: db.Mapped[int] = db.mapped_column(nullable=False)
    is_event: db.Mapped[bool] = db.mapped_column(nullable=False)
    identifier: db.Mapped[str] = db.mapped_column(db.String(50), nullable=False)

    parent_id = db.mapped_column(db.ForeignKey("alerts.id"))
    references: db.Mapped[List["Alert"]] = db.relationship("Alert")

    states: db.Mapped[List["State"]] = db.relationship(back_populates="alert")

    PER_PAGE = 20

    @staticmethod
    def get_references(identifiers: list[str]) -> list["Alert"]:
        """ Get the alerts referenced by the alert with given id.
        """
        alert_refs = []
        for id_ in identifiers:
            alert = db.session.execute(
                db.select(Alert).filter_by(identifier=id_)).scalar_one()
            alert_refs.append(alert)
        return alert_refs

    @staticmethod
    def get_by_date(date: str):
        """ Get all alerts that match a specific date.
            Time is not considered, only date.

            Dates must be given in iso-format.
        """
        date = datetime.date.fromisoformat(date)
        return db.session.execute(
            db.select(Alert).filter(
                func.date(Alert.time) == date
            )
        ).scalars().all()

    @staticmethod
    def get_by_date_range(start: str, end: str, desc: bool = False):
        """ Get all alerts in the range from start to end (both inclusive).

            Dates must be given in iso-format.
        """
        start_date = datetime.date.fromisoformat(start)
        end_date = datetime.date.fromisoformat(end)

        if not desc:
            return db.session.execute(
                db.select(Alert)
                .filter(
                    func.date(Alert.time) >= start_date,
                    func.date(Alert.time) <= end_date
                )
            ).scalars().all()
        else:
            return db.session.execute(
                db.select(Alert)
                .filter(
                    func.date(Alert.time) >= start_date,
                    func.date(Alert.time) <= end_date
                )
                .order_by(Alert.time.desc())
            ).scalars().all()

    @staticmethod
    def get_by_identifier(identifier: str) -> Optional["Alert"]:
        """ Get the alert with the given identifier.
        """
        if identifier == "latest":
            return db.session.execute(
                db.select(Alert).order_by(Alert.time.desc())
            ).scalars().first()
        else:
            return db.session.execute(
                db.select(Alert).filter_by(identifier=identifier)).scalar_one_or_none()

    @staticmethod
    def get_by_state_code(code: str, page: int = 1) -> tuple[list["Alert"], int, int, int]:
        """ Get all alerts in the given state in descending order of time.
        """
        code_int = int(code)
        select = db.select(Alert)\
            .join(State)\
            .filter(State.state_id == code_int)\
            .order_by(Alert.time.desc())
        pagination = db.paginate(select, page=page, per_page=Alert.PER_PAGE)
        return (
            pagination.items,
            pagination.prev_num,
            pagination.next_num,
            pagination.total
        )

    @staticmethod
    def get_by_region(region: str, page: int = 1) -> tuple[list["Alert"], int, int, int]:
        """ Get all alerts that match the given region in descending order.

            Uses pagination.

            Note that a region name can correspond to different codes.

            :param region: Name of the region without spaces and in lowe case.
            :param page: The page to retrieve.

        """
        region_codes = None
        for reg, codes in REGION_CODES.items():
            reg_lower = "".join(reg.lower().split())
            if reg_lower == region:
                region_codes = codes
                break

        if region_codes is None:
            raise ValueError(f"Invalid region {region}")

        select = db.select(Alert)\
            .filter(Alert.region.in_(region_codes))\
            .order_by(Alert.time.desc())
        pagination = db.paginate(select, page=page, per_page=Alert.PER_PAGE)
        return (
            pagination.items,
            pagination.prev_num,
            pagination.next_num,
            pagination.total
        )

    @staticmethod
    def get_pagination(page: int = 1) -> tuple[list["Alert"], int, int, int]:
        """ Returns the paginated alerts in descending order of date.
        """
        select = db.select(Alert).order_by(Alert.time.desc())
        pagination = db.paginate(select, page=page, per_page=Alert.PER_PAGE)
        return (
            pagination.items,
            pagination.prev_num,
            pagination.next_num,
            pagination.total
        )

    @staticmethod
    def get_non_events(page: int = 1) -> tuple[list["Alert"], int, int, int]:
        """ Returns the paginated alerts which are not events in descending order of date.
        """
        select = db.select(Alert).filter_by(is_event=False).order_by(Alert.time.desc())
        pagination = db.paginate(select, page=page, per_page=Alert.PER_PAGE)
        return (
            pagination.items,
            pagination.prev_num,
            pagination.next_num,
            pagination.total
        )

    @staticmethod
    def get_events(page: int = 1) -> tuple[list["Alert"], int, int, int]:
        """ Returns the paginated events in descending order of date.
        """
        select = db.select(Alert).filter_by(is_event=True).order_by(Alert.time.desc())
        pagination = db.paginate(select, page=page, per_page=Alert.PER_PAGE)
        return (
            pagination.items,
            pagination.prev_num,
            pagination.next_num,
            pagination.total
        )

    @staticmethod
    def from_json(json: dict[str, Any]) -> "Alert":
        """ Construct an Alert from a json object
        """
        references = Alert.get_references(json["references"])
        states = [State(state_id=s) for s in json["states"]]
        alert = Alert(
            time=datetime.datetime.fromisoformat(json["time"]),
            states=states,
            region=json["region"],
            is_event=json["is_event"],
            identifier=json["id"],
            references=references
        )
        db.session.add(alert)
        return alert

    def to_cap_file(self) -> str:
        """ Returns the contents of a cap file representing this alert."""
        cap_alert = self.to_cap_alert()
        feed = create_feed(cap_alert)
        return feed.content

    def to_cap_alert(self) -> CapAlert:
        refs = [ref.to_cap_alert() for ref in self.references]
        if len(refs) == 0:
            refs = None
        return CapAlert(
            time=self.time,
            states=[s.state_id for s in self.states],
            region=self.region,
            id=self.identifier,
            is_event=self.is_event,
            refs=refs
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "time": self.time.isoformat(timespec="seconds"),
            "states": [s.state_id for s in self.states],
            "region": self.region,
            "is_event": self.is_event,
            "id": self.identifier,
            "references": [ref.to_json() for ref in self.references],
        }

    def save_to_file(self, path: str, logger: logging.Logger) -> None:
        cap_alert = self.to_cap_alert()
        feed = create_feed(cap_alert)
        save_path = os.path.join(path, f"sasmex.xml")
        try:
            with open(save_path, "w") as fp:
                fp.write(feed.content)
            logger.info(f"Saved cap file to {path}")
        except IOError as e:
            logger.debug(f"Failed to save cap file {path}")
            logger.debug(e)

    def __repr__(self) -> str:
        return f"Alert(id={self.id}, time={self.time}, " \
               f"region={self.region}, identifier={self.identifier})"


class State(db.Model):
    __tablename__ = "states"
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    state_id: db.Mapped[int] = db.mapped_column(nullable=False)
    alert_id: db.Mapped[int] = db.mapped_column(db.ForeignKey("alerts.id"))

    alert: db.Mapped[Alert] = db.relationship(back_populates="states")

    def __repr__(self) -> str:
        return f"State(id={self.id}, state_id={self.state_id})"


def query_alerts(
        page: int = 1,
        alert_type: Literal["alert", "event", "all"] = "all",
        start_date: str = "",
        end_date: str = "",
        region: str = "",
        state: str = ""
) -> tuple[list["Alert"], int, int, int]:
    """ Query the alerts model, optionally apply multiple filters. Returns
        alerts paginated and in descending order of date.
    """
    pass
