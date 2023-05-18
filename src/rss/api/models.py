from rss.api import db


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

    @staticmethod
    def get_references(identifiers: list[str]) -> list["Alert"]:
        alert_refs = []
        for id_ in identifiers:
            alert = db.session.execute(
                db.select(Alert).filter_by(identifier=id_)).scalar_one()
            alert_refs.append(alert)
        return alert_refs

    def __repr__(self) -> str:
        return f"Alert(id={self.id}, time={self.time}, " \
               f"city={self.city}, identifier={self.identifier})"
