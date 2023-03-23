from datetime import datetime

from rss import rss
from rss.alert import Alert


def alert():
    return Alert(
        time=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
        city=40,
        region=42201,
        polygons=[(16.12, -94.36, 18.30, -94.06, 16.97, -91.50, 15.45, -93.27, 16.12, -94.36)],
        geocoords=(16.12309, -95.42281)
    )


def get_feed():
    return rss.RSSFeed(alert())


def header(entry, updated_date):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xml:lang="es-MX" xmlns:georss="http://www.georss.org/georss" xmlns="http://www.w3.org/2005/Atom">
<id>https://rss.sasmex.net</id>
<link type="text/html" rel="alternate" href="https://rss.sasmex.net"/>
<link type="application/atom+xml" rel="self" href="https://rss.sasmex.net/sasmex2.xml"/>
<title>SASMEX-CIRES RSS Feed</title>
<subtitle>Sistema de Alerta Sísmica Mexicano</subtitle>
<updated>{updated_date}</updated>
<logo>https://rss.sasmex.net/ciresFeedLogo2b.png</logo>
<icon>https://rss.sasmex.net/ciresFeedFavicon.ico</icon>
<author>
<name>CIRES A.C.</name>
<email>infoCAP@cires-ac.mx</email>
</author>
{entry}
</feed>
"""


def entry_tag(content, updated_date):
    return f"""<entry>
<id>20233131675</id>
<updated>{updated_date}</updated>
<title>13 Mar 2023 16:07:05 Alerta en CDMX por sismo en Costa Oax-Gro</title>
<author>
<name>CIRES A.C.</name>
</author>
<georss:point>16.12309 -95.42281</georss:point>
<georss:elev>0</georss:elev>
<summary>Sismo</summary>{content}
</entry>
"""


def content_tag(info):
    return f"""<content type="text/xml">
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.1">
<identifier>20233131675</identifier>
<sender>sasmex.net</sender>
<sent>2023-03-13T16:07:05</sent>
<status>Actual</status>
<msgType>Alert</msgType>
<scope>Public</scope>
<code>IPAWSv1.0</code>
<note>Requested by=Cires,Activated by=AGG</note>
<references>sasmex.net,20233131675,2023-03-13T16:07:05</references>{info}
</alert>
</content>
"""


def info_tag():
    return f"""<info>
<language>es-MX</language>
<category>Geo</category>
<event>Alerta por sismo</event>
<responseType>Prepare</responseType>
<urgency>Past</urgency>
<severity>Major</severity>
<certainty>Observed</certainty>
<effective>2023-03-13T16:07:05</effective>
<expires>2023-03-13T16:08:05</expires>
<senderName>Sistema de Alerta Sísmica Mexicano</senderName>
<headline>Alerta Sísmica</headline>
<description>SASMEX registró un sismo</description>
<instruction>Realice procedimiento en caso de sismo</instruction>
<web>http://sasmex.net</web>
<contact>CIRES</contact>
<eventCode>
<valueName>SAME</valueName>
<value>EQW</value>
</eventCode>
<parameter>
<valueName>Id</valueName>
<value>20233131675</value>
</parameter>
<parameter>
<valueName>EAS</valueName>
<value>1</value>
</parameter>
<parameter>
<valueName>EventID</valueName>
<value>S42212T1678745171458</value>
</parameter>
<resource>
<resourceDesc>Image file (GIF)</resourceDesc>
<mimeType>image/gif</mimeType>
<uri>http://www.sasmex.net/sismos/getAdvisoryImage</uri>
</resource>
<area>
<areaDesc>Zona de emisión de alerta</areaDesc>
<polygon>16.12,-94.36,18.30,-94.06,16.97,-91.50,15.45,-93.27,16.12,-94.36</polygon>
<geocode>
<valueName>SAME</valueName>
<value>009000</value>
</geocode>
</area>
</info>
"""


def test_create_header():
    feed = get_feed()
    feed._create_header()
    content = feed._root.toprettyxml(indent='', encoding="UTF-8").decode()

    expected = header("<entry/>", feed._updated_date)
    expected = expected.split('\n')

    assert content.split('\n') == expected


def test_create_entry_tag():
    feed = get_feed()
    entry = feed._root.createElement("entry")
    feed._root.appendChild(entry)
    feed._create_entry_tag(entry)
    content = feed._root.toprettyxml(indent="")

    expected = entry_tag("", feed._updated_date)
    expected = expected.split('\n')

    # skip xml declaration
    assert content.split('\n')[1:] == expected


def test_create_content_tag():
    expected = content_tag("")
    expected = expected.split('\n')

    feed = get_feed()
    content, _ = feed._create_content_tag()

    content_str = content.toprettyxml(indent="")
    assert content_str.split('\n') == expected


def test_create_info_tag():
    expected = info_tag()
    expected = expected.split('\n')

    feed = get_feed()
    content = feed._create_info_tag()

    content_str = content.toprettyxml(indent="")
    assert content_str.split('\n') == expected


def test_create_rss_feed():
    feed = rss.create_feed(alert=alert(), indentation="")

    content = content_tag('\n' + info_tag())
    entry = entry_tag('\n' + content, feed._updated_date)
    root = header(entry, feed._updated_date)

    feed_content = feed.content.split('\n')
    feed_content = [s for s in feed_content if len(s) > 0]

    expected = root.split('\n')
    expected = [s for s in expected if len(s) > 0]
    assert feed_content == expected
