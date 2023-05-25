import datetime
import random

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from rss.config import configurations
from rss.api import create_app, db
from rss.api.models import Alert
from rss.cap.services import MessageProcessor
from rss.cap.data import CITIES, REGIONS


def clear_database() -> None:
    engine = create_engine(configurations["dev"].SQLALCHEMY_DATABASE_URI)
    engine.connect()
    session = sessionmaker(bind=engine)()

    # Clear database after running tests
    session.execute(text("DELETE FROM alerts"))
    session.commit()
    session.close()


def generate_fake_alerts():
    """ Generate fake alerts and put then in the database.
    """
    clear_database()

    app = create_app(configurations["dev"])

    end_date = datetime.date.today()
    end_date = datetime.datetime(year=end_date.year, month=end_date.month, day=end_date.day)
    start_date = end_date - datetime.timedelta(days=365)
    print(f"Start date: {start_date}")
    print(f"End date: {end_date}")

    dates = []
    current_date = start_date
    time_delta = datetime.timedelta(days=1)
    while current_date <= end_date:
        dates.append(current_date)
        current_date += time_delta

    options = (True, False)
    day_choices = random.choices(
        options,
        weights=[0.5, 0.5],
        k=len(dates))
    event_choices = random.choices(
        options,
        weights=[0.2, 0.8],
        k=len(dates))
    references_choices = random.choices(
        options,
        weights=[0.4, 0.6],
        k=len(dates))

    cities = list(CITIES.keys())
    regions = list(REGIONS)

    id_list = []
    with app.app_context():
        for ii in range(len(dates)):
            if day_choices[ii]:
                identifier = MessageProcessor.alert_id(dates[ii])
                city = random.choice(cities)
                region = random.choice(regions)

                if references_choices[ii] and ii > 1:
                    # Reference the previous alert
                    references = Alert.get_references([id_list[-1]])
                    alert = Alert(
                        time=dates[ii],
                        city=city,
                        region=region,
                        is_event=event_choices[ii],
                        identifier=identifier,
                        references=references
                    )
                else:
                    alert = Alert(
                        time=dates[ii],
                        city=city,
                        region=region,
                        is_event=event_choices[ii],
                        identifier=identifier,
                    )

                db.session.add(alert)
                db.session.commit()
                print(f"Added new alert {alert}")
                id_list.append(identifier)

        n_alerts = len(db.session.execute(db.select(Alert)).all())
        print(f"Total number of alerts {n_alerts}")

    print(id_list)


if __name__ == "__main__":
    print("Adding new alerts to DB")
    generate_fake_alerts()
    print("DONE")
