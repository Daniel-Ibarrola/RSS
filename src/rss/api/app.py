from datetime import datetime
from flask import abort, request, jsonify
from flask_migrate import Migrate

from rss import CONFIG
from rss.api import create_app, db
from rss.api.models import Alert


app = create_app(CONFIG)
migrate = Migrate(app, db)
api_route = "/api/v1"


def handle_error(error_type: str, status_code: int):
    response = jsonify({"error": error_type})
    response.status_code = status_code
    return response


@app.errorhandler(403)
def forbidden(e):
    return handle_error("forbidden", 403)


@app.errorhandler(404)
def page_not_found(e):
    return handle_error("not found", 404)


@app.errorhandler(500)
def internal_server_error(e):
    return handle_error("internal server error", 500)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Alert=Alert)


@app.route("/")
def index():
    return "OK", 200


@app.route(f"{api_route}/new_alert", methods=["POST"])
def add_new_alert():
    references = Alert.get_references(request.json["references"])
    alert = Alert(
        time=datetime.fromisoformat(request.json["time"]),
        city=request.json["city"],
        region=request.json["region"],
        is_event=request.json["is_event"],
        identifier=request.json["id"],
        references=references
    )
    db.session.add(alert)
    db.session.commit()
    return "Ok", 201


@app.route(f"{api_route}/alerts/<identifier>")
def get_alert(identifier):
    alert = db.session.execute(
        db.select(Alert).filter_by(identifier=identifier)).scalar_one_or_none()
    if alert is None:
        abort(404)
    return jsonify(alert.to_json())


@app.route(f"{api_route}/alerts/dates/<date>")
def get_alerts_by_date(date):
    alerts = Alert.get_by_date(date)
    if len(alerts) == 0:
        abort(404)
    return jsonify({
        "alerts": [al.to_json() for al in alerts]
    })


@app.route(f"{api_route}/alerts/")
def get_alerts():
    page = request.args.get("page", 1, type=int)
    alerts, prev, next_page, total = Alert.get_pagination(page)
    if len(alerts) == 0:
        abort(404)
    return jsonify({
        "alerts": [al.to_json() for al in alerts],
        "prev": prev,
        "next": next_page,
        "count": total,
    })


@app.route(f"{api_route}/cap/<identifier>")
def get_cap_file(identifier):
    alert = db.session.execute(
        db.select(Alert).filter_by(identifier=identifier)).scalar_one_or_none()
    if alert is None:
        abort(404)
    file_contents = alert.to_cap_file()
    return jsonify({
        "contents": file_contents
    })
