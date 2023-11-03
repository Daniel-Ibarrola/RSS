from flask import Response

from alerts import CONFIG, create_app, db
from alerts.errors import errors
from alerts.alerts.models import Alert
from alerts.utils.fake import generate_fake_alerts
from alerts.utils.wait_for_db import wait_for_postgres


app = create_app()
api_route = "/api/v1"


@app.errorhandler(400)
def bad_request(error) -> Response:
    return errors.bad_request("Invalid request")


@app.errorhandler(401)
def unauthorized(error) -> Response:
    return errors.unauthorized("Invalid Credentials")


@app.errorhandler(403)
def forbidden(error) -> Response:
    return errors.forbidden("Forbidden")


@app.errorhandler(404)
def page_not_found(error) -> Response:
    return errors.not_found("The requested resource could not be found")


@app.errorhandler(500)
def internal_server_error(error) -> Response:
    return errors.bad_request("There was an error handling your request")


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Alert=Alert)


@app.route("/ping")
def index():
    return {"message": "ok"}


@app.cli.command("wait-for-db")
def wait_for_db():
    """ Wait for the database to start. """
    postgres_uri = CONFIG.SQLALCHEMY_DATABASE_URI
    if "dev" in CONFIG.NAME:
        print(f"Attempting to connect to database in {postgres_uri}.")
    else:
        print(f"Attempting to connect to database.")
    wait_for_postgres(postgres_uri)


@app.cli.command("seed-db")
def seed_db():
    """ Add multiple alerts to the database.
    """
    generate_fake_alerts()
