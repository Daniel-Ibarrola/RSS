import datetime
from typing import Any
from sqlalchemy import func

from rss.api import db
from rss.cap.alert import Alert as CapAlert
from rss.cap.rss import create_feed


class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.TIMESTAMP, nullable=False)
    city = db.Column(db.Integer, nullable=False)
    region = db.Column(db.Integer, nullable=False)
    is_event = db.Column(db.Boolean, nullable=False)
    identifier = db.Column(db.String(50), nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey("alerts.id"))
    references = db.relationship("Alert")

    PER_PAGE = 20

    @staticmethod
    def get_references(identifiers: list[str]) -> list["Alert"]:
        alert_refs = []
        for id_ in identifiers:
            alert = db.session.execute(
                db.select(Alert).filter_by(identifier=id_)).scalar_one()
            alert_refs.append(alert)
        return alert_refs

    @staticmethod
    def get_by_date(date: str):
        """ Get all alerts that match a specific date.
            Time is not considered.
        """
        date = datetime.date.fromisoformat(date)
        alerts = db.session.execute(
            db.select(Alert).filter(
                func.date(Alert.time) == date
            )
        ).scalars().all()
        return alerts

    @staticmethod
    def get_pagination(page: int = 1):
        select = db.select(Alert).order_by(Alert.time)
        pagination = db.paginate(select, page=page, per_page=Alert.PER_PAGE)
        return (
            pagination.items,
            pagination.prev_num,
            pagination.next_num,
            pagination.total
        )

    def to_cap_file(self) -> str:
        cap_alert = self.to_cap_alert()
        feed = create_feed(cap_alert)
        return feed.content

    def to_cap_alert(self) -> CapAlert:
        refs = [ref.to_cap_alert() for ref in self.references]
        if len(refs) == 0:
            refs = None
        return CapAlert(
            time=self.time,
            city=self.city,
            region=self.region,
            id=self.identifier,
            is_event=self.is_event,
            refs=refs
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "time": self.time.isoformat(timespec="seconds"),
            "city": self.city,
            "region": self.region,
            "is_event": self.is_event,
            "id": self.identifier,
            "references": [ref.to_json() for ref in self.references],
        }

    def __repr__(self) -> str:
        return f"Alert(id={self.id}, time={self.time}, " \
               f"city={self.city}, identifier={self.identifier})"
