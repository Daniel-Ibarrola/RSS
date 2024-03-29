from collections import defaultdict
from rss.cap.polygon import GeoPoint

# Lat and long of each region
REGION_COORDS = {
    40101: GeoPoint(lat=19.38714, lon=-99.15771),
    40102: GeoPoint(lat=19.314858, lon=-99.174865),
    40103: GeoPoint(lat=19.424536, lon=-99.118108),
    41101: GeoPoint(lat=17.53542, lon=-99.49944),
    41102: GeoPoint(lat=16.86917, lon=-99.89293),
    42101: GeoPoint(lat=17.05115, lon=-96.72295),
    43101: GeoPoint(lat=19.702071, lon=-101.192894),
    44101: GeoPoint(lat=19.23427, lon=-103.7065),
    45101: GeoPoint(lat=20.62926, lon=-103.33643),
    46101: GeoPoint(lat=19.04531, lon=-98.19902),
    47101: GeoPoint(lat=18.959409, lon=-99.232145),
    41201: GeoPoint(lat=17.29717, lon=-101.04279),
    41202: GeoPoint(lat=17.21729, lon=-100.78777),
    41203: GeoPoint(lat=17.16214, lon=-100.63043),
    41204: GeoPoint(lat=17.12559, lon=-100.3504),
    41205: GeoPoint(lat=17.01392, lon=-100.11742),
    41206: GeoPoint(lat=16.88257, lon=-99.94501),
    41207: GeoPoint(lat=16.83026, lon=-99.7321),
    41208: GeoPoint(lat=16.78042, lon=-99.5011),
    41209: GeoPoint(lat=16.75872, lon=-99.2331),
    41210: GeoPoint(lat=16.63958, lon=-99.02931),
    41211: GeoPoint(lat=16.59523, lon=-98.81599),
    41212: GeoPoint(lat=16.63599, lon=-98.56606),
    41213: GeoPoint(lat=17.49615, lon=-101.24909),
    41214: GeoPoint(lat=17.60673, lon=-101.46517),
    41215: GeoPoint(lat=17.74216, lon=-101.63146),
    41216: GeoPoint(lat=17.78421, lon=-101.71952),
    41217: GeoPoint(lat=17.93527, lon=-101.80595),
    41218: GeoPoint(lat=17.992, lon=-101.92287),
    41219: GeoPoint(lat=18.36917, lon=-100.68334),
    41220: GeoPoint(lat=18.0683, lon=-100.52297),
    41221: GeoPoint(lat=18.36545, lon=-100.17848),
    41222: GeoPoint(lat=17.95861, lon=-100.02152),
    41223: GeoPoint(lat=18.34053, lon=-99.69362),
    41224: GeoPoint(lat=17.92505, lon=-99.37268),
    41225: GeoPoint(lat=18.33573, lon=-99.19035),
    41226: GeoPoint(lat=17.77376, lon=-98.72038),
    41227: GeoPoint(lat=17.82988, lon=-98.9854),
    41228: GeoPoint(lat=17.98514, lon=-101.21552),
    41229: GeoPoint(lat=17.09681, lon=-99.8061),
    41230: GeoPoint(lat=17.00646, lon=-99.46076),
    41231: GeoPoint(lat=16.96152, lon=-99.08932),
    41232: GeoPoint(lat=16.81131, lon=-98.74218),
    41233: GeoPoint(lat=16.8788, lon=-98.36163),
    42201: GeoPoint(lat=16.30636, lon=-98.44299),  # This one
    42202: GeoPoint(lat=16.53936, lon=-98.25224),
    42203: GeoPoint(lat=16.67263, lon=-98.04842),
    42204: GeoPoint(lat=16.29569, lon=-97.90988),
    42205: GeoPoint(lat=16.12813, lon=-97.60101),
    42206: GeoPoint(lat=16.2388, lon=-97.21663),
    42207: GeoPoint(lat=15.97637, lon=-97.06948),
    42208: GeoPoint(lat=15.79657, lon=-96.71954),
    42209: GeoPoint(lat=15.66288, lon=-96.49927),
    42210: GeoPoint(lat=15.77712, lon=-96.09455),
    42211: GeoPoint(lat=16.02188, lon=-95.66643),
    42212: GeoPoint(lat=16.12309, lon=-95.42281),
    42213: GeoPoint(lat=16.26784, lon=-95.59278),
    42214: GeoPoint(lat=16.40066, lon=-95.76279),
    42215: GeoPoint(lat=17.17457, lon=-96.65342),
    42216: GeoPoint(lat=16.5921, lon=-97.22521),
    42217: GeoPoint(lat=16.48783, lon=-96.98431),
    42218: GeoPoint(lat=16.47158, lon=-96.70268),
    42219: GeoPoint(lat=16.2048, lon=-96.41342),
    42220: GeoPoint(lat=17.5863, lon=-97.41789),
    42221: GeoPoint(lat=17.35862, lon=-97.94788),
    42222: GeoPoint(lat=17.96579, lon=-98.06949),
    42223: GeoPoint(lat=17.39174, lon=-97.27546),
    42224: GeoPoint(lat=17.56843, lon=-96.49979),
    42225: GeoPoint(lat=18.0077, lon=-96.27092),
    42226: GeoPoint(lat=18.22989, lon=-96.40981),
    42227: GeoPoint(lat=18.19804, lon=-97.67599),
    42228: GeoPoint(lat=16.56256, lon=-97.53823),
    42229: GeoPoint(lat=17.05115, lon=-96.72295),
    42230: GeoPoint(lat=18.04529, lon=-97.69287),
    42231: GeoPoint(lat=17.11383, lon=-96.45668),
    42232: GeoPoint(lat=17.05633, lon=-96.06096),
    42233: GeoPoint(lat=17.34154, lon=-95.37379),
    42234: GeoPoint(lat=16.68732, lon=-95.52353),
    42235: GeoPoint(lat=16.37487, lon=-95.27271),
    42236: GeoPoint(lat=16.74151, lon=-95.09448),
    42237: GeoPoint(lat=17.06505, lon=-96.7035),
    42238: GeoPoint(lat=17.62253, lon=-98.34422),
    42239: GeoPoint(lat=18.17493, lon=-97.03688),
    43201: GeoPoint(lat=18.04544, lon=-102.18918),
    43202: GeoPoint(lat=18.02455, lon=-102.49857),
    43203: GeoPoint(lat=18.08557, lon=-102.75306),
    43204: GeoPoint(lat=18.20923, lon=-103.00048),
    43205: GeoPoint(lat=18.28844, lon=-103.34562),
    43206: GeoPoint(lat=18.46423, lon=-103.54034),
    43207: GeoPoint(lat=18.62549, lon=-103.66751),
    43208: GeoPoint(lat=18.26979, lon=-101.89481),
    43209: GeoPoint(lat=18.53522, lon=-101.32374),
    44201: GeoPoint(lat=18.8195, lon=-103.69816),
    44202: GeoPoint(lat=18.95922, lon=-103.96115),
    44203: GeoPoint(lat=19.05661, lon=-104.224),
    44204: GeoPoint(lat=19.15444, lon=-104.44947),
    44205: GeoPoint(lat=19.19108, lon=-104.68021),
    45201: GeoPoint(lat=19.35123, lon=-104.89204),
    45202: GeoPoint(lat=19.57213, lon=-105.08386),
    45203: GeoPoint(lat=19.67493, lon=-105.17883),
    45204: GeoPoint(lat=19.90173, lon=-105.31767),
    45205: GeoPoint(lat=20.02962, lon=-105.47832),
    45206: GeoPoint(lat=20.30982, lon=-105.47994),
    46201: GeoPoint(lat=18.24111, lon=-98.70637),
    46202: GeoPoint(lat=18.33549, lon=-98.26213),
    46203: GeoPoint(lat=18.58894, lon=-97.91219),
    46204: GeoPoint(lat=18.68977, lon=-97.65844),
    46205: GeoPoint(lat=18.48049, lon=-97.37209),
    48201: GeoPoint(lat=18.89936, lon=-96.93618),
    48202: GeoPoint(lat=18.56161, lon=-96.8478),
    48203: GeoPoint(lat=18.4471, lon=-96.35641),
    48204: GeoPoint(lat=18.12644, lon=-95.82659),
    48205: GeoPoint(lat=17.82697, lon=-95.81803),
    48206: GeoPoint(lat=17.8092, lon=-95.22087),
    48207: GeoPoint(lat=17.66808, lon=-95.14166),
    48208: GeoPoint(lat=17.38456, lon=-94.98834),
    48209: GeoPoint(lat=17.2099, lon=-94.20324),
    49201: GeoPoint(lat=16.17234, lon=-94.06314),
    49202: GeoPoint(lat=16.72522, lon=-93.80817),
    49203: GeoPoint(lat=17.1887, lon=-93.60444),
    49204: GeoPoint(lat=16.75384, lon=-93.09278),
    49205: GeoPoint(lat=16.42922, lon=-93.4441),
    49206: GeoPoint(lat=15.86586, lon=-93.63254),
    49207: GeoPoint(lat=16.73643, lon=-92.63257),
    49208: GeoPoint(lat=16.33469, lon=-92.56102),
    49209: GeoPoint(lat=16.04022, lon=-92.81878),
    49210: GeoPoint(lat=15.43169, lon=-92.89934),
    49211: GeoPoint(lat=16.90722, lon=-92.08311),
    49212: GeoPoint(lat=16.24173, lon=-92.12366),
    49213: GeoPoint(lat=15.83068, lon=-92.03312),
    49214: GeoPoint(lat=15.36401, lon=-92.24822),
    49215: GeoPoint(lat=15.13878, lon=-92.46471),
    49216: GeoPoint(lat=14.89802, lon=-92.26555),
    41301: GeoPoint(lat=17.70099, lon=-98.74409),
    41302: GeoPoint(lat=17.42286, lon=-99.52309),
    41303: GeoPoint(lat=17.56598, lon=-99.46616),
    41304: GeoPoint(lat=16.91193, lon=-99.8966),
    41305: GeoPoint(lat=16.59523, lon=-98.81599),
    41306: GeoPoint(lat=17.01392, lon=-100.11742),
    41307: GeoPoint(lat=17.16214, lon=-100.63043),
    41308: GeoPoint(lat=17.29717, lon=-101.04279),
    41309: GeoPoint(lat=17.64847, lon=-101.5823),
    41310: GeoPoint(lat=18.59675, lon=-99.59796),
    41311: GeoPoint(lat=18.04321, lon=-99.90873),
    41312: GeoPoint(lat=18.42154, lon=-99.98237),
    41313: GeoPoint(lat=16.67938, lon=-98.44528),
    42301: GeoPoint(lat=16.3892, lon=-98.0414),
    42302: GeoPoint(lat=16.2388, lon=-97.21663),
    42303: GeoPoint(lat=15.66288, lon=-96.49927),
    42304: GeoPoint(lat=16.2048, lon=-96.41342),
    42305: GeoPoint(lat=16.26784, lon=-95.59278),
    42306: GeoPoint(lat=17.17457, lon=-96.65342),
    42307: GeoPoint(lat=17.56843, lon=-96.49979),
    42308: GeoPoint(lat=17.35862, lon=-97.94788),
    42309: GeoPoint(lat=17.5863, lon=-97.41789),
    42310: GeoPoint(lat=18.04529, lon=-97.69287),
    42311: GeoPoint(lat=17.11383, lon=-96.45668),
    42312: GeoPoint(lat=18.17493, lon=-97.03688),
    43301: GeoPoint(lat=18.34632, lon=-102.34539),
    43302: GeoPoint(lat=18.18252, lon=-103.01479),
    43303: GeoPoint(lat=18.29097, lon=-103.38023),
    43304: GeoPoint(lat=18.61249, lon=-103.62922),
    44301: GeoPoint(lat=19.05987, lon=-103.82371),
    44302: GeoPoint(lat=19.14871, lon=-104.40399),
    45301: GeoPoint(lat=20.59394, lon=-103.46968),
    45302: GeoPoint(lat=19.56564, lon=-103.61671),
    45303: GeoPoint(lat=19.63449, lon=-104.94679),
    45304: GeoPoint(lat=20.42561, lon=-105.45584),
    47301: GeoPoint(lat=19.08809, lon=-99.14873),
    40401: GeoPoint(lat=19.38714, lon=-99.15771),
    40402: GeoPoint(lat=19.314858, lon=-99.174865),
    40403: GeoPoint(lat=19.424536, lon=-99.118108),
    41401: GeoPoint(lat=17.53542, lon=-99.49944),
    41402: GeoPoint(lat=16.86917, lon=-99.89293),
    42401: GeoPoint(lat=17.05115, lon=-96.72295),
    43401: GeoPoint(lat=19.702071, lon=-101.192894),
    44401: GeoPoint(lat=19.23427, lon=-103.7065),
    45401: GeoPoint(lat=20.62926, lon=-103.33643),
    46401: GeoPoint(lat=19.04531, lon=-98.19902),
    47401: GeoPoint(lat=18.959409, lon=-99.23214),
}

REGIONS = {
    41201: 'Petatlan Gro',
    41202: 'Petatlan Gro',
    41203: 'Atoyac Gro',
    41204: 'Guerrero',
    41205: 'Atoyac Gro',
    41206: 'Acapulco Gro',
    41207: 'Acapulco Gro',
    41208: 'SanMarcos Gro',
    41209: 'Guerrero',
    41210: 'Guerrero',
    41211: 'SanMarcos Gro',
    41212: 'Costa Gro-Oax',
    41213: 'Petatlan Gro',
    41214: 'Petatlan Gro',
    41215: 'Zihuatanejo Gro',
    41216: 'Guerrero',
    41217: 'Zihuatanejo Gro',
    41218: 'Costa Gro-Mich',
    41219: 'Guerrero',
    41220: 'Guerrero',
    41221: 'Guerrero',
    41222: 'Guerrero',
    41223: 'Guerrero',
    41224: 'Guerrero',
    41225: 'Guerrero',
    41226: 'Guerrero',
    41227: 'Guerrero',
    41228: 'Guerrero',
    41229: 'Guerrero',
    41230: 'Guerrero',
    41231: 'Guerrero',
    41232: 'Guerrero',
    41233: 'Guerrero',
    41301: 'Guerrero',
    41302: 'Guerrero',
    41303: 'Guerrero',
    41304: 'Guerrero',
    41305: 'Guerrero',
    41306: 'Guerrero',
    41307: 'Guerrero',
    41308: 'Guerrero',
    41309: 'Guerrero',
    41310: 'Guerrero',
    41311: 'Guerrero',
    41312: 'Guerrero',
    41313: 'Guerrero',
    41401: 'Guerrero',
    41402: 'Guerrero',
    42101: 'Guerrero',
    42201: 'Costa Oax-Gro',
    42202: 'Oaxaca',
    42203: 'Costa Oax-Gro',
    42204: 'Pinotepa Oax',
    42205: 'Pinotepa Oax',
    42206: 'PtoEscondido Oax',
    42207: 'Oaxaca',
    42208: 'PtoEscondido Oax',
    42209: 'Huatulco Oax',
    42210: 'Oaxaca',
    42211: 'Huatulco Oax',
    42212: 'SalinaCruz Oax',
    42213: 'Oaxaca',
    42214: 'SalinaCruz Oax',
    42215: 'Oax Centro',
    42216: 'Oaxaca',
    42217: 'Oaxaca',
    42218: 'Oax Centro',
    42219: 'Huatulco Oax',
    42220: 'Huajuapan Oax',
    42221: 'Huajuapan Oax',
    42222: 'Lim Oax-Pue',
    42223: 'Oax Centro',
    42224: 'Oax Centro',
    42225: 'Tuxtepec Oax',
    42226: 'Tuxtepec Oax',
    42227: 'Lim Oax-Pue',
    42228: 'Oax Centro',
    42229: 'Oax Centro',
    42230: 'Lim Oax-Pue',
    42231: 'Oax Centro',
    42232: 'Oax Centro',
    42233: 'Lim Ver-Oax',
    42234: 'Istmo Oax-Chis',
    42235: 'Oaxaca',
    42236: 'Istmo Oax-Chis',
    42237: 'Oax Centro',
    42238: 'Oaxaca',
    42239: 'Oaxaca',
    42301: 'Oaxaca',
    42302: 'Oaxaca',
    42303: 'Oaxaca',
    42304: 'Oaxaca',
    42305: 'Oaxaca',
    42306: 'Oaxaca',
    42307: 'Oaxaca',
    42308: 'Oaxaca',
    42309: 'Oaxaca',
    42310: 'Oaxaca',
    42311: 'Oaxaca',
    42312: 'Oaxaca',
    42401: 'Oaxaca',
    43101: 'Oaxaca',
    43201: 'Costa Mich-Gro',
    43202: 'Playa Azul Mich',
    43203: 'Playa Azul Mich',
    43204: 'Costa Mich',
    43205: 'Costa Mich',
    43206: 'Costa Mich',
    43207: 'Costa Mich-Col',
    43208: 'Costa Mich',
    43209: 'Costa Mich',
    43301: 'Costa Mich',
    43302: 'Costa Mich',
    43303: 'Costa Mich',
    43304: 'Costa Mich',
    43401: 'Costa Mich',
    44101: 'Costa Mich',
    44201: 'Costa Col',
    44202: 'Costa Col',
    44203: 'Costa Col',
    44204: 'Costa Col',
    44205: 'Costa Col',
    44301: 'Costa Col',
    44302: 'Costa Col',
    44401: 'Costa Col',
    45101: 'Costa Col',
    45201: 'Costa Jal',
    45202: 'Costa Jal',
    45203: 'Costa Jal',
    45204: 'Costa Jal',
    45205: 'Costa Jal',
    45206: 'Costa Jal',
    45301: 'Costa Jal',
    45302: 'Costa Jal',
    45303: 'Costa Jal',
    45304: 'Costa Jal',
    45401: 'Costa Jal',
    46101: 'Costa Jal',
    46201: 'Puebla',
    46202: 'Puebla',
    46203: 'Puebla',
    46204: 'Puebla',
    46205: 'Puebla',
    46401: 'Puebla',
    47101: 'Puebla',
    47301: 'Morelos',
    47401: 'Morelos',
    48201: 'Veracruz',
    48202: 'Veracruz',
    48203: 'Veracruz',
    48204: 'Veracruz',
    48205: 'Veracruz',
    48206: 'Veracruz',
    48207: 'Veracruz',
    48208: 'Veracruz',
    48209: 'Veracruz',
    49201: 'Chiapas',
    49202: 'Chiapas',
    49203: 'Chiapas',
    49204: 'Chiapas',
    49205: 'Chiapas',
    49206: 'Chiapas',
    49207: 'Chiapas',
    49208: 'Chiapas',
    49209: 'Chiapas',
    49210: 'Chiapas',
    49211: 'Chiapas',
    49212: 'Chiapas',
    49213: 'Chiapas',
    49214: 'Chiapas',
    49215: 'Chiapas',
    49216: 'Chiapas',
}


def region_codes_map() -> dict[str, set[int]]:
    """ Returns a map of the region name to region codes.

        A region can have multiple codes
    """
    region_codes = defaultdict(set)
    for code, region in REGIONS.items():
        region_codes[region].add(code)
    return region_codes


REGION_CODES = region_codes_map()

