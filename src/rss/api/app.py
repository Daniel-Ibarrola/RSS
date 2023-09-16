import os.path

from flask import current_app, request, jsonify, Response
from flask_httpauth import HTTPBasicAuth

from rss.api import API_CONFIG, create_app, db
from rss.api import errors
from rss.api.models import Alert, get_alerts_by_type
from rss.utils.wait_for_db import wait_for_postgres


app = create_app()
auth = HTTPBasicAuth()
api_route = "/api/v1"


@auth.verify_password
def verify_password(user: str, password: str) -> bool:
    return user == API_CONFIG.API_USER and password == API_CONFIG.API_PASSWORD


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


@app.route(f"{api_route}/new_alert", methods=["POST"])
@auth.login_required
def add_new_alert():
    alert = Alert.from_json(request.json)
    save_path = request.args.get("save_path", "")
    current_app.logger.info(f"Path {save_path}")
    if save_path and os.path.isdir(save_path):
        alert.save_to_file(save_path, current_app.logger)
    db.session.commit()
    # TODO: respond with json that contains the alert id
    return "Ok", 201


@app.route(f"{api_route}/alerts/<identifier>")
def get_alert(identifier):
    alert = Alert.get_by_identifier(identifier)
    if alert is not None:
        return jsonify(alert.to_json())
    return errors.not_found(f"Alert with identifier {identifier} could not be found")


@app.route(f"{api_route}/alerts/dates/<date>")
def get_alerts_by_date(date):
    end_date = request.args.get("end", "")
    if not end_date:
        alerts = Alert.get_by_date(date)
    else:
        alerts = Alert.get_by_date_range(date, end_date)
    if len(alerts) > 0:
        return jsonify({
            "alerts": [al.to_json() for al in alerts]
        })
    return errors.not_found(f"No alerts found with date {date}")


@app.route(f"{api_route}/alerts/")
def get_alerts():
    alert_type = request.args.get("type", "all")
    page = request.args.get("page", 1, type=int)
    if alert_type not in {"all", "alert", "event"}:
        return errors.bad_request("Invalid alert type")

    alerts, prev, next_page, total = get_alerts_by_type(alert_type, page)
    if len(alerts) > 0:
        return jsonify({
            "alerts": [al.to_json() for al in alerts],
            "prev": prev,
            "next": next_page,
            "count": total,
        })
    return errors.not_found("No alerts found")


@app.route(f"{api_route}/cap_contents/<identifier>")
def get_cap_file_contents(identifier):
    alert = Alert.get_by_identifier(identifier)
    if alert is not None:
        file_contents = alert.to_cap_file()
        return jsonify({
            "contents": file_contents
        })
    return errors.not_found(f"Alert with identifier {identifier} could not be found")


@app.route(f"{api_route}/cap/<identifier>")
def get_cap_file(identifier):
    alert = Alert.get_by_identifier(identifier)
    if alert is not None:
        file_contents = alert.to_cap_file()
        if identifier == "latest":
            identifier = "sasmex"
        response = Response(file_contents, mimetype="text/xml")
        response.headers.set(
            "Content-Disposition", "attachment", filename=f"{identifier}.cap"
        )
        return response
    return errors.not_found(f"Alert with identifier {identifier} could not be found")


@app.route(f"{api_route}/last_alert/")
def get_last_alert():
    alert = Alert.get_by_identifier("latest")
    if alert is not None:
        return jsonify(alert.to_json())
    return errors.not_found("No alerts found")


@app.route(f"{api_route}/regions/<region>")
def get_alerts_by_region(region):
    page = request.args.get("page", 1, type=int)
    alerts, prev, next_page, total = Alert.get_by_region(region, page)
    if len(alerts) > 0:
        return jsonify({
            "alerts": [al.to_json() for al in alerts],
            "prev": prev,
            "next": next_page,
            "count": total,
        })
    return errors.not_found("No alerts found")


@app.route(f"{api_route}/states/<state_code>")
def get_alerts_by_state(state_code):
    page = request.args.get("page", 1, type=int)
    alerts, prev, next_page, total = Alert.get_by_state_code(state_code, page)
    if len(alerts) > 0:
        return jsonify({
            "alerts": [al.to_json() for al in alerts],
            "prev": prev,
            "next": next_page,
            "count": total,
        })
    return errors.not_found("No alerts found")


@app.cli.command("wait-for-db")
def wait_for_db():
    """ Wait for the database to start. """
    postgres_uri = API_CONFIG.SQLALCHEMY_DATABASE_URI
    print(f"Attempting to connect to database in {postgres_uri}")
    wait_for_postgres(postgres_uri)
