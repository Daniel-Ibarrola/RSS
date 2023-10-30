import os.path

from flask import current_app, request, jsonify, Response
from flask_httpauth import HTTPBasicAuth

from rss.api import API_CONFIG, db
from rss.api.alerts import api
from rss.api.alerts.models import Alert, query_alerts
from rss.api.errors import errors


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(user: str, password: str) -> bool:
    return user == API_CONFIG.API_USER and password == API_CONFIG.API_PASSWORD


@api.route("/alerts/", methods=["POST"])
@auth.login_required
def add_new_alert():
    """ Add new alert to the database.
    """
    id_ = request.json["id"]
    if Alert.get_by_identifier(id_) is not None:
        return errors.bad_request(f"Alert with identifier {id_} already exists")

    alert = Alert.from_json(request.json)
    save_path = request.args.get("save_path", "")

    if save_path and os.path.isdir(save_path):
        alert.save_to_file(save_path, current_app.logger)

    db.session.commit()
    return jsonify(alert.to_json()), 201


@api.route("/alerts/")
def get_alerts():
    """ Get multiple alerts. Results are paginated.

        Can optionally pas multiple filters as url parameters. Valid
        filters are:
        - type
        - page
        - start_date
        - end_date
        - region
        - state
    """

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


@api.route("/alerts/<identifier>/")
def get_alert(identifier):
    """ Returns the alert with the given identifier.

        If identifier is set to 'latest', the latest alert will be returned.

    """
    alert = Alert.get_by_identifier(identifier)
    if alert is not None:
        return jsonify(alert.to_json())
    return errors.not_found(f"Alert with identifier {identifier} could not be found")


@api.route("/cap/latest")
def latest_cap_file():
    """ Get the latest alert as a cap file.

        This route is deprecated and will be removed in the future.
        Please use the alerts/latest/cap/ instead.
    """
    alert = Alert.get_by_identifier("latest")
    if alert is not None:
        file_contents = alert.to_cap_file()
        response = Response(file_contents, mimetype="text/xml")
        response.headers.set(
            "Content-Disposition", "attachment", filename="sasmex.cap"
        )
        return response
    return errors.not_found(f"No alerts were found")


@api.route("/alerts/<identifier>/cap/")
def get_cap_file(identifier):
    """ Returns a cap file for the alert with the given identifier.

        If identifier is set to 'latest', the latest alert will be returned.

    """
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
