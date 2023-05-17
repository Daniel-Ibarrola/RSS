from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from rss import CONFIG

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(CONFIG)

    db.init_app(app)

    return app
