from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from rss import CONFIG
from rss.config import DevConfig

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    if isinstance(CONFIG, DevConfig):
        CORS(app)
    Migrate(app, db)
    return app
