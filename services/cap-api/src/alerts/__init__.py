from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os

from alerts.config import Config, DevConfig, api_configs

db = SQLAlchemy()
CONFIG = api_configs[os.environ.get("CONFIG", "dev")]


def create_app(configuration: Config = CONFIG):
    app = Flask(__name__)
    app.config.from_object(configuration)

    db.init_app(app)

    from alerts.alerts import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    if isinstance(configuration, DevConfig):
        CORS(app)

    Migrate(app, db)
    return app
