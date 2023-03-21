from datetime import datetime
from rss import rss


def location():
    return rss.Location(
        name="Salina Cruz Oaxaca",
        geocoords=(16.12309, -95.42281),
        latitude=15.82,
        longitude=-95.52,
        depth=38,
        how_far=55
    )


def get_feed():
    return rss.RSSFeed(
        event_id="S42212T1678745171458-1678747055210",
        date=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
        location=location(),
        event="Sismo ligero",
        nearest="42212 Mazatán SV",
        magnitude=4.1
    )


def header(entry):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xml:lang="es-MX" xmlns:georss="http://www.georss.org/georss" xmlns="http://www.w3.org/2005/Atom">
<id>https://rss.sasmex.net</id>
<link type="text/html" rel="alternate" href="https://rss.sasmex.net"/>
<link type="application/atom+xml" rel="self" href="https://rss.sasmex.net/sasmex2.xml"/>
<title>SASMEX-Cires Rss Feed</title>
<subtitle>Sistema de Alerta Sísmica Mexicano</subtitle>
<updated>2023-03-13T16:07:05</updated>
<logo>https://rss.sasmex.net/ciresFeedLogo2b.png</logo>
<icon>https://rss.sasmex.net/ciresFeedFavicon.ico</icon>
<author>
<name>Cires A.C.</name>
<email>infoCAP@cires-ac.mx</email>
</author>
{entry}
</feed>
"""


def entry_tag(content):
    return f"""<entry>
<id>S42212T1678745171458-1678745225150</id>
<updated>2023-03-13T16:07:05</updated>
<title>13 Mar 2023 16:07:05 Sismo Fuerte</title>
<author>
<name>Cires A.C.</name>
</author>
<georss:point>16.12309 -95.42281</georss:point>
<georss:elev>0</georss:elev>
<summary>Sismo ligero</summary>{content}
</entry>
"""


def content_tag(info):
    return f"""<content type="text/xml">
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.1">
<identifier>S42212T1678745171458-1678745225150</identifier>
<sender>sasmex.net</sender>
<sent>2023-03-13T16:07:05</sent>
<status>Actual</status>
<msgType>Alert</msgType>
<scope>Public</scope>
<code>IPAWSv1.0</code>
<note>Requested by=Cires,Activated by=AGG</note>
<references>sasmex.net,S42212T1678745171458-1678745225148,2023-03-13T16:07:05</references>{info}
</alert>
</content>
"""


def info_tag():
    return f"""<info>
<language>es-MX</language>
<category>Geo</category>
<event>Sismo ligero</event>
<responseType>Prepare</responseType>
<urgency>Past</urgency>
<severity>Minor</severity>
<certainty>Observed</certainty>
<effective>2023-03-13T16:07:05</effective>
<expires>2023-03-13T16:07:05</expires>
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
<value>S42212T1678745171458-1678745225150</value>
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
    expected = header("<entry/>")
    expected = expected.split('\n')

    feed = get_feed()
    feed._create_header()
    content = feed._root.toprettyxml(indent='', encoding="UTF-8").decode()
    assert content.split('\n') == expected


def test_create_entry_tag():
    expected = entry_tag("")
    expected = expected.split('\n')

    feed = get_feed()
    entry = feed._root.createElement("entry")
    feed._root.appendChild(entry)
    feed._create_entry_tag(entry)

    content = feed._root.toprettyxml(indent="")
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
    content = content_tag('\n' + info_tag())
    entry = entry_tag('\n' + content)
    root = header(entry)
    expected = root.split('\n')
    expected = [s for s in expected if len(s) > 0]

    feed = rss.create_feed(
        event_id="S42212T1678745171458-1678747055210",
        date=datetime(year=2023, month=3, day=13, hour=16, minute=7, second=5),
        location=location(),
        event="Sismo ligero",
        nearest="42212 Mazatán SV",
        magnitude=4.1,
        indentation=""
    )

    feed_content = feed.content.split('\n')
    feed_content = [s for s in feed_content if len(s) > 0]
    assert feed_content == expected