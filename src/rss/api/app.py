from datetime import datetime
from flask import request
from flask_migrate import Migrate

from rss import CONFIG
from rss.api import create_app, db
from rss.api.models import Alert


app = create_app(CONFIG)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return "OK", 200


@app.route("/api/v1/new_alert", methods=["POST"])
def add_new_alert():
    refs = Alert.get_references(request.json["refs"])
    alert = Alert(
        time=datetime.fromisoformat(request.json["time"]),
        city=request.json["city"],
        region=request.json["region"],
        is_event=request.json["is_event"],
        identifier=request.json["id"],
        references=refs
    )
    alert.add_references(refs)
    db.session.add(alert)
    db.session.commit()
    return "Ok", 201
