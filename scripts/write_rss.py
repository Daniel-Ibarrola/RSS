from datetime import datetime
from rss import rss


def main():
    location = rss.Location(
        name="Salina Cruz Oaxaca",
        geocoords=(16.12309, -95.42281),
        latitude=15.82,
        longitude=-95.52,
        depth=38,
        how_far=55
    )
    feed = rss.create_feed(
        event_id="S42212T1678745171458-1678747055210",
        date=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
        location=location,
        event="Sismo ligero",
        nearest="42212 Mazatán SV",
        magnitude=4.1,
    )

    rss.write_feed_to_file("sasmex.xml", feed)


if __name__ == "__main__":
    main()
    print("DONE")
