import os.path

from flask import abort, current_app, request, jsonify, Response
from flask_httpauth import HTTPBasicAuth

from rss import CONFIG
from rss.api import create_app, db
from rss.api.models import Alert
from rss.utils.wait_for_db import wait_for_postgres


app = create_app(CONFIG)
auth = HTTPBasicAuth()
api_route = "/api/v1"


@auth.verify_password
def verify_password(user: str, password: str) -> bool:
    return user == CONFIG.API_USER and password == CONFIG.API_PASSWORD


def handle_error(error_type: str, status_code: int):
    response = jsonify({"error": error_type})
    response.status_code = status_code
    return response


@app.errorhandler(401)
def unauthorized(message: str) -> Response:
    return handle_error("unauthorized", 401)


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
@auth.login_required
def add_new_alert():
    alert = Alert.from_json(request.json)
    save_path = request.args.get("save_path", "")
    current_app.logger.info(f"Path {save_path}")
    if save_path and os.path.isdir(save_path):
        alert.save_to_file(save_path, current_app.logger)
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


@app.route(f"{api_route}/cap_contents/<identifier>")
def get_cap_file_contents(identifier):
    if identifier == "latest":
        alert = db.session.execute(
            db.select(Alert).order_by(Alert.time.desc())
        ).scalars().first()
    else:
        alert = db.session.execute(
            db.select(Alert).filter_by(identifier=identifier)).scalar_one_or_none()
    if alert is None:
        abort(404)
    file_contents = alert.to_cap_file()
    return jsonify({
        "contents": file_contents
    })


@app.route(f"{api_route}/cap/<identifier>")
def get_cap_file(identifier):
    if identifier == "latest":
        alert = db.session.execute(
            db.select(Alert).order_by(Alert.time.desc())
        ).scalars().first()
    else:
        alert = db.session.execute(
            db.select(Alert).filter_by(identifier=identifier)).scalar_one_or_none()
    if alert is None:
        abort(404)
    file_contents = alert.to_cap_file()
    if identifier == "latest":
        identifier = "sasmex"

    response = Response(file_contents, mimetype="text/xml")
    response.headers.set(
        "Content-Disposition", "attachment", filename=f"{identifier}.cap"
    )
    return response


@app.route(f"{api_route}/last_alert/")
def get_last_alert():
    alert = db.session.execute(
        db.select(Alert).order_by(Alert.time.desc())
    ).scalars().first()
    if alert is None:
        abort(404)
    return jsonify(alert.to_json())


@app.cli.command("wait-for-db")
def wait_for_db():
    """ Wait for the database to start. """
    postgres_uri = CONFIG.SQLALCHEMY_DATABASE_URI
    print(f"Attempting to connect to database in {postgres_uri}")
    wait_for_postgres(postgres_uri)
