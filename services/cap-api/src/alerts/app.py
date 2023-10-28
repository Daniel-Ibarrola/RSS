import os.path

from flask import current_app, request, jsonify, Response
from flask_httpauth import HTTPBasicAuth

from alerts import CONFIG, create_app, db
from alerts.errors import errors
from alerts.alerts.models import Alert, query_alerts
from alerts.utils.wait_for_db import wait_for_postgres


app = create_app()
auth = HTTPBasicAuth()
api_route = "/api/v1"


@auth.verify_password
def verify_password(user: str, password: str) -> bool:
    return user == CONFIG.API_USER and password == CONFIG.API_PASSWORD


@app.errorhandler(400)
def bad_request(error):
    return errors.bad_request("Invalid request")


@app.errorhandler(401)
def unauthorized(error) -> Response:
    return errors.unauthorized("Invalid Credentials")


@app.errorhandler(403)
def forbidden(error):
    return errors.forbidden("Forbidden")


@app.errorhandler(404)
def page_not_found(error):
    return errors.not_found("The requested resource could not be found")


@app.errorhandler(500)
def internal_server_error(error):
    return errors.bad_request("There was an error handling your request")


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Alert=Alert)


@app.route("/")
def index():
    return "OK", 200


@app.route(f"{api_route}/alerts/", methods=["POST"])
@auth.login_required
def add_new_alert():
    id_ = request.json["id"]
    if Alert.get_by_identifier(id_) is not None:
        return errors.bad_request(f"Alert with identifier {id_} already exists")

    alert = Alert.from_json(request.json)
    save_path = request.args.get("save_path", "")

    if save_path and os.path.isdir(save_path):
        alert.save_to_file(save_path, current_app.logger)
    db.session.commit()
    return jsonify(alert.to_json()), 201


@app.route(f"{api_route}/alerts/<identifier>")
def get_alert(identifier):
    alert = Alert.get_by_identifier(identifier)
    if alert is not None:
        return jsonify(alert.to_json())
    return errors.not_found(f"Alert with identifier {identifier} could not be found")


@app.route(f"{api_route}/alerts/")
def get_alerts():
    alert_type = request.args.get("type", "all")
    page = request.args.get("page", 1, type=int)
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    region = request.args.get("region", "")
    state = request.args.get("state", "")

    if alert_type not in {"all", "alert", "event"}:
        return errors.bad_request(f"Invalid alert type {alert_type}")

    alerts, prev, next_page, total = query_alerts(
        page, alert_type, start_date, end_date, region, state)
    return jsonify({
        "alerts": [al.to_json() for al in alerts],
        "prev": prev,
        "next": next_page,
        "count": total,
    })


@app.route(f"{api_route}/alerts/<identifier>/cap/")
def get_cap_file(identifier):
    save_file = request.args.get("save", "false")

    alert = Alert.get_by_identifier(identifier)
    if alert is not None:
        file_contents = alert.to_cap_file()
        if save_file.lower() == "true":
            if identifier == "latest":
                identifier = "sasmex"
            response = Response(file_contents, mimetype="text/xml")
            response.headers.set(
                "Content-Disposition", "attachment", filename=f"{identifier}.cap"
            )
            return response
        else:
            return jsonify({
                "contents": file_contents
            })
    return errors.not_found(f"Alert with identifier {identifier} could not be found")


@app.route(f"{api_route}/alerts/latest/")
def get_last_alert():
    alert = Alert.get_by_identifier("latest")
    if alert is not None:
        return jsonify(alert.to_json())
    return errors.not_found("No latest alerts found")


@app.cli.command("wait-for-db")
def wait_for_db():
    """ Wait for the database to start. """
    postgres_uri = CONFIG.SQLALCHEMY_DATABASE_URI
    print(f"Attempting to connect to database in {postgres_uri}")
    wait_for_postgres(postgres_uri)