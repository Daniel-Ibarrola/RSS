from rss.api import db


class Reference(db.Model):
    __tablename__ = "references"
    alert_id = db.Column(db.Integer, db.ForeignKey("alerts.id"), primary_key=True)
    reference_id = db.Column(db.Integer, db.ForeignKey("alerts.id"), primary_key=True)


class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.TIMESTAMP, nullable=False)
    city = db.Column(db.Integer, nullable=False)
    region = db.Column(db.Integer, nullable=False)
    is_event = db.Column(db.Boolean, nullable=False)
    identifier = db.Column(db.String(50), nullable=False)

    # Alerts this alert references
    referencing = db.relationship(
        "Reference",
        foreign_keys=[Reference.alert_id],
        backref=db.backref("referenced_by", lazy="joined"),
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    # Alerts referencing this alert
    referenced_by = db.relationship(
        "Reference",
        foreign_keys=[Reference.reference_id],
        backref=db.backref("referencing", lazy="joined"),
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

    def add_references(self, references: list[str]) -> None:
        for identifier in references:
            alert = db.session.execute(
                db.select(Alert).filter_by(identifier=identifier)).first()
            if alert is None:
                continue
            ref = Reference(referencing=alert, referenced_by=self)
            db.session.add(ref)
