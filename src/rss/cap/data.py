from dataclasses import dataclass


@dataclass(frozen=True)
class GeoPoint:
    lon: float
    lat: float


@dataclass(frozen=True)
class Polygon:
    points: list[GeoPoint]


CITIES = {
    40: 'CDMX',
    41: 'Guerrero',
    42: 'Oaxaca',
    43: 'Michoacán',
    44: 'Colima',
    45: 'Jalisco',
    46: 'Puebla',
    47: 'Morelos',
    48: 'Veracruz',
    49: 'Chiapas',
}

POLYGONS = {
    40: Polygon([
        GeoPoint(-98.23597442933914, 17.92411146620965),
        GeoPoint(-97.73105697385562, 19.71178820720766),
        GeoPoint(-100.2567253728701, 20.36337783147095),
        GeoPoint(-100.8044251457549, 18.72329481693715),
        GeoPoint(-98.23597442933914, 17.92411146620965),
    ]),
    41: Polygon([
        GeoPoint(-98.07862978825065, 16.0110296092669),
        GeoPoint(-97.54593323457897, 17.8415966116602),
        GeoPoint(-101.8761975763345, 19.2879448824476),
        GeoPoint(-102.5378210264313, 17.7258083999512),
        GeoPoint(-98.07862978825065, 16.0110296092669),
    ]),
    42: Polygon([
        GeoPoint(-94.06228754859151, 15.47721897238834),
        GeoPoint(-93.87265942984988, 18.35477333359784),
        GeoPoint(-98.59345543761631, 18.54701348538807),
        GeoPoint(-98.70231961564679, 15.62069465224437),
        GeoPoint(-94.06228754859151, 15.47721897238834),
    ]),
    43: Polygon([
        GeoPoint(-100.3082496102006, 19.22258227299296),
        GeoPoint(-99.90574894221695, 20.25137939386669),
        GeoPoint(-101.7004679199828, 20.98750980416739),
        GeoPoint(-102.5163263850749, 20.04819533305848),
        GeoPoint(-100.3082496102006, 19.22258227299296),
    ]),
    44: Polygon([
        GeoPoint(-102.1736180920661, 17.52391478191304),
        GeoPoint(-100.1106393437513, 19.34135457963665),
        GeoPoint(-103.1835224398227, 20.50015872501815),
        GeoPoint(-104.95654982688, 19.06711470238654),
        GeoPoint(-102.1736180920661, 17.52391478191304),
    ]),
    45: Polygon([
        GeoPoint(-104.2491058523325, 18.38044565693096),
        GeoPoint(-101.3397552345668, 20.92694779732655),
        GeoPoint(-102.6629224869377, 22.03350792252786),
        GeoPoint(-106.3991102388304, 20.90634816402552),
        GeoPoint(-104.2491058523325, 18.38044565693096),
    ]),
    46: Polygon([

    ]),
    47: Polygon([

    ]),
    48: Polygon([
        GeoPoint(-93.25305668675571, 17.42108253392388),
        GeoPoint(-93.12916347987822, 18.52870348672094),
        GeoPoint(-97.73072782213934, 20.6891868605619),
        GeoPoint(-98.45648071083687, 18.1953653038331),
        GeoPoint(-93.25305668675571, 17.42108253392388),
    ]),
    49: Polygon([
        GeoPoint(-93.27134825264807, 15.45412744189985),
        GeoPoint(-91.50417117489262, 16.99065334514076),
        GeoPoint(-94.04488228807821, 18.2991028252503),
        GeoPoint(-94.3660249339337, 16.12904295556978),
        GeoPoint(-93.27134825264807, 15.45412744189985),
    ])
}


def get_region(region_code: int) -> str:
    # TODO: convert this code into a hash table
    if region_code > 49200:
        return "Chiapas"
    elif region_code > 48200:
        return "Veracruz"
    elif region_code > 47200:
        return 'Morelos'
    elif region_code > 46200:
        return 'Puebla'
    elif region_code > 45200:
        return 'Costa Jal'
    elif region_code > 44200:
        return 'Costa Col'
    elif region_code > 43200:
        n1 = region_code - 43200
        if n1 == 1:
            return "Costa Mich-Gro"
        elif n1 in [2, 3]:
            return "Playa Azul Mich"
        elif n1 == 7:
            return "Costa Mich-Col"
        else:
            return "Costa Mich"
    elif region_code > 42200:
        n1 = region_code - 42200
        if n1 in [1, 3]:
            return 'Costa Oax-Gro'
        if n1 in [4, 5]:
            return 'Pinotepa Oax'
        if n1 in [6, 8]:
            return 'PtoEscondido Oax'
        if n1 in [9, 11]:
            return 'Huatulco Oax'
        if n1 in [12, 14]:
            return 'SalinaCruz Oax'
        if n1 in [15, 18]:
            return 'Oax Centro'
        if n1 in [19]:
            return 'Huatulco Oax'
        if n1 in [20, 21]:
            return 'Huajuapan Oax'
        if n1 in [22]:
            return 'Lim Oax-Pue'
        if n1 in [23, 24]:
            return 'Oax Centro'
        if n1 in [25, 26]:
            return 'Tuxtepec Oax'
        if n1 in [27]:
            return 'Lim Oax-Pue'
        if n1 in [28, 29]:
            return 'Oax Centro'
        if n1 in [30]:
            return 'Lim Oax-Pue'
        if n1 in [31, 32]:
            return 'Oax Centro'
        if n1 in [33]:
            return 'Lim Ver-Oax'
        if n1 in [34, 36]:
            return 'Istmo Oax-Chis'
        if n1 in [37]:
            return 'Oax Centro'
        else:
            return 'Oaxaca'
    elif region_code > 41200:
        n1 = region_code - 41200
        if n1 in [1, 2]:
            return 'Petatlan Gro'
        if n1 in [3, 5]:
            return 'Atoyac Gro'
        if n1 in [6, 7]:
            return 'Acapulco Gro'
        if n1 in [8, 11]:
            return 'SanMarcos Gro'
        if n1 in [12]:
            return 'Costa Gro-Oax'
        if n1 in [13, 14]:
            return 'Petatlan Gro'
        if n1 in [15, 17]:
            return 'Zihuatanejo Gro'
        if n1 in [18]:
            return 'Costa Gro-Mich'
        else:
            return 'Guerrero'
    return ""


COORDS = {
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
    42201: GeoPoint(lat=16.30636, lon=-98.44299),
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
 40101,
 40102,
 40103,
 41101,
 41102,
 42101,
 43101,
 44101,
 45101,
 46101,
 47101,
 41201,
 41202,
 41203,
 41204,
 41205,
 41206,
 41207,
 41208,
 41209,
 41210,
 41211,
 41212,
 41213,
 41214,
 41215,
 41216,
 41217,
 41218,
 41219,
 41220,
 41221,
 41222,
 41223,
 41224,
 41225,
 41226,
 41227,
 41228,
 41229,
 41230,
 41231,
 41232,
 41233,
 42201,
 42202,
 42203,
 42204,
 42205,
 42206,
 42207,
 42208,
 42209,
 42210,
 42211,
 42212,
 42213,
 42214,
 42215,
 42216,
 42217,
 42218,
 42219,
 42220,
 42221,
 42222,
 42223,
 42224,
 42225,
 42226,
 42227,
 42228,
 42229,
 42230,
 42231,
 42232,
 42233,
 42234,
 42235,
 42236,
 42237,
 42238,
 42239,
 43201,
 43202,
 43203,
 43204,
 43205,
 43206,
 43207,
 43208,
 43209,
 44201,
 44202,
 44203,
 44204,
 44205,
 45201,
 45202,
 45203,
 45204,
 45205,
 45206,
 46201,
 46202,
 46203,
 46204,
 46205,
 48201,
 48202,
 48203,
 48204,
 48205,
 48206,
 48207,
 48208,
 48209,
 49201,
 49202,
 49203,
 49204,
 49205,
 49206,
 49207,
 49208,
 49209,
 49210,
 49211,
 49212,
 49213,
 49214,
 49215,
 49216,
 41301,
 41302,
 41303,
 41304,
 41305,
 41306,
 41307,
 41308,
 41309,
 41310,
 41311,
 41312,
 41313,
 42301,
 42302,
 42303,
 42304,
 42305,
 42306,
 42307,
 42308,
 42309,
 42310,
 42311,
 42312,
 43301,
 43302,
 43303,
 43304,
 44301,
 44302,
 45301,
 45302,
 45303,
 45304,
 47301,
 40401,
 40402,
 40403,
 41401,
 41402,
 42401,
 43401,
 44401,
 45401,
 46401,
 47401,
}
