from datetime import datetime
import pytest
from rss import rss


@pytest.fixture
def location():
    return rss.Location(
        name="Salina Cruz Oaxaca",
        geocoords=(16.12309, -95.42281),
        latitude=15.82,
        longitude=-95.52,
        depth=38,
        how_far=53
    )


def test_create_header(location):
    expected = """<?xml version="1.0" ?>
<feed xml:lang="es-MX">
<id>https://rss.sasmex.net</id>
<link type="text/html" rel="alternate" href="https://rss.sasmex.net"/>
<link type="application/atom+xml" rel="self" href="https://rss.sasmex.net/sasmex2.xml"/>
<title>SASMEX-Cires Rss Feed</title>
<subtitle>Sistema de Alerta Sísmica Mexicano</subtitle>
<updated>2023-03-13T22:37:35</updated>
<logo>https://rss.sasmex.net/ciresFeedLogo2b.png</logo>
<icon>https://rss.sasmex.net/ciresFeedFavicon.ico</icon>
<author>
<name>Cires A.C.</name>
<email>infoCAP@cires-ac.mx</email>
</author>
<entry/>
<entry/>
</feed>
"""
    expected = expected.split('\n')

    feed = rss.RSSFeed(
        event_id="S42212T1678745171458-1678747055210",
        date=datetime(year=2023, month=3, day=13, hour=22, minute=37, second=35),
        location=location,
        event="Sismo ligero",
        nearest="42212 Mazatán SV",
        magnitude=4.1
    )
    feed._create_header()
    content = feed._root.toprettyxml(indent='')
    assert content.split('\n') == expected


def test_create_entry_tag(location):
    expected = """<?xml version="1.0" ?>
<entry>
<id>S42212T1678745171458-1678745225150</id>
<updated>2023-03-13T16:07:05</updated>
<title>13 Mar 2023 16:07:05 Sismo ligero en Salina Cruz Oaxaca - Actualización</title>
<author>
<name>Cires A.C.</name>
</author>
<georss:point>16.12309 -95.42281</georss:point>
<georss:elev>0</georss:elev>
<summary>Sismo ligero</summary>
</entry>
"""
    expected = expected.split('\n')

    feed = rss.RSSFeed(
        event_id="S42212T1678745171458-1678747055210",
        date=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
        location=location,
        event="Sismo ligero",
        nearest="42212 Mazatán SV",
        magnitude=4.1
    )
    entry = feed._root.createElement("entry")
    feed._root.appendChild(entry)
    feed._create_entry_tag(entry)

    content = feed._root.toprettyxml(indent="")
    assert content.split('\n') == expected


def test_create_rss_feed(location):
    feed = rss.create_feed(
        event_id="S42212T1678745171458-1678747055210",
        date=datetime(year=2023, month=3, day=13, hour=7, minute=5, second=6),
        location=location,
        event="Sismo ligero",
        nearest="42212 Mazatán SV",
        magnitude=4.1,
        indentation=""
    )

    feed_content = feed.content.split('\n')
    assert feed_content == expected_feed()
