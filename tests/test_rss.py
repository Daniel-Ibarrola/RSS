from datetime import datetime

import pytest

from rss import rss


def expected_feed():
    feed = """<?xml version="1.0" ?>
<feed xml:lang="es-MX" xmlns="http://www.w3.org/2005/Atom" xmlns:georss="http://www.georss.org/georss">
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
<entry>
<id>S42212T1678745171458-1678745225150</id>
<updated>2023-03-13T16:07:05-06:00</updated>
<title>13 Mar 2023 16:06:11 Sismo Ligero en Salina Cruz Oaxaca - Actualización</title>
<author>
<name>Cires A.C.</name>
</author>
<georss:point>16.12309 -95.42281</georss:point>
<georss:elev>0</georss:elev>
<summary>Sismo de efectos estimados ligeros</summary>
<content type="text/xml">
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.1">
<identifier>S42212T1678745171458-1678745225150</identifier>
<sender>sasmex.net</sender>
<sent>2023-03-13T16:07:05-06:00</sent>
<status>Actual</status>
<msgType>Alert</msgType>
<scope>Public</scope>
<references>sasmex.net,S42212T1678745171458-1678745225148,2023-03-13T16:07:05-06:00</references>
<info>
<language>es-MX</language>
<category>Geo</category>
<event>Sismo Ligero</event>
<urgency>Past</urgency>
<severity>Minor</severity>
<certainty>Observed</certainty>
<expires>2023-03-14T16:06:11-06:00</expires>
<senderName>Sistema de Alerta Sísmica Mexicano</senderName>
<headline>Sismo Ligero en Salina Cruz Oaxaca</headline>
<description>El 13 Mar 2023 16:06:11 el SASMEX registró un sismo que fue evaluado y confirmado por sensores próximos a su epicentro. La estimación de sus efectos es de un sismo Ligero. La estación más cercana al epicentro que detectó el sismo es la número 42212 Mazatán SV, localizada a 25 km al Oeste Suroeste de Salina Cruz, Oaxaca, 55 km al Suroeste de Juchitan, Oaxaca.
</description>
<web>http://sasmex.net</web>
<parameter>
<valueName>Id</valueName>
<value>S42212T1678745171458-1678745225150</value>
</parameter>
<parameter>
<valueName>EventID</valueName>
<value>S42212T1678745171458</value>
</parameter>
<parameter>
<valueName>layer:Google:Region:0.1</valueName>
<value>Salina Cruz Oaxaca</value>
</parameter>
<parameter>
<valueName>SsnInfo</valueName>
<value>Esperando información</value>
</parameter>
<area>
<areaDesc>Sismo Registrado por la estación 42212 Mazatán SV localizada a 25 km al Oeste Suroeste de Salina Cruz, Oaxaca; 55 km al Suroeste de Juchitan, Oaxaca</areaDesc>
<circle>16.12309,-95.42281 50.0</circle>
</area>
</info>
</alert>
</content>
</entry>
<entry>
<id>S42212T1678745171458-1678747055210</id>
<updated>2023-03-13T16:37:35-06:00</updated>
<title>13 Mar 2023 16:06:11 Sismo Ligero en Salina Cruz Oaxaca - Actualización</title>
<author>
<name>Cires A.C.</name>
</author>
<georss:point>16.12309 -95.42281</georss:point>
<georss:elev>0</georss:elev>
<summary>Sismo de efectos estimados ligeros</summary>
<content type="text/xml">
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.1">
<identifier>S42212T1678745171458-1678747055210</identifier>
<sender>sasmex.net</sender>
<sent>2023-03-13T16:37:35-06:00</sent>
<status>Actual</status>
<msgType>Update</msgType>
<scope>Public</scope>
<references>sasmex.net,S42212T1678745171458-1678745225148,2023-03-13T16:07:05-06:00 sasmex.net,S42212T1678745171458-1678745225150,2023-03-13T16:07:05-06:00 sasmex.net,S42212T1678745171458-1678747055206,2023-03-13T16:37:35-06:00</references>
<info>
<language>es-MX</language>
<category>Geo</category>
<event>Sismo Ligero</event>
<urgency>Past</urgency>
<severity>Minor</severity>
<certainty>Observed</certainty>
<expires>2023-03-14T16:06:11-06:00</expires>
<senderName>Sistema de Alerta Sísmica Mexicano</senderName>
<headline>Sismo Ligero en Salina Cruz Oaxaca</headline>
<description>El 13 Mar 2023 16:06:11 el SASMEX registró un sismo que fue evaluado y confirmado por sensores próximos a su epicentro. La estimación de sus efectos es de un sismo Ligero. La estación más cercana al epicentro que detectó el sismo es la número 42212 Mazatán SV.
De acuerdo a la información proporcionada por el Servicio Sismológico Nacional, el sismo se originó a las 16:06:02 del 13 Mar 2023, tuvo una magnitud de 4.1, se localizó a 53 km al Suroeste de Salina Cruz Oax en la latitud 15.82 y longitud -95.52 a una profundidad de 38 km.
</description>
<web>http://sasmex.net</web>
<parameter>
<valueName>Id</valueName>
<value>S42212T1678745171458-1678747055210</value>
</parameter>
<parameter>
<valueName>EventID</valueName>
<value>S42212T1678745171458</value>
</parameter>
<parameter>
<valueName>layer:Google:Region:0.1</valueName>
<value>53 km al Suroeste de Salina Cruz Oax</value>
</parameter>
<parameter>
<valueName>SsnInfo</valueName>
<value>SISMO Magnitud 4.1 Loc. 53 km al Suroeste de Salina Cruz Oax 13 Mar 2023 16:06:02 Lat 15.82 Lon -95.52 Pf 38 km</value>
</parameter>
<area>
<areaDesc>53 km al Suroeste de Salina Cruz Oax</areaDesc>
<circle>15.82,-95.52 50.0</circle>
</area>
</info>
</alert>
</content>
</entry>
</feed>"""
    return feed.split("\n")


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
