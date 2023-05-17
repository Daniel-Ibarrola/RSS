from flask_migrate import Migrate
from rss.api import create_app, db


app = create_app()
migrate = Migrate(app, db)


@app.route("/")
def index():
    return "OK", 200
