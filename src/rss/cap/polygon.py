from dataclasses import dataclass
from rss.cap.geopoint import GeoPoint


@dataclass(frozen=True)
class Polygon:
    points: list[GeoPoint]


POLYGONS = {
    "CDMX": Polygon([
        GeoPoint(-98.23597442933914, 17.92411146620965),
        GeoPoint(-97.73105697385562, 19.71178820720766),
        GeoPoint(-100.2567253728701, 20.36337783147095),
        GeoPoint(-100.8044251457549, 18.72329481693715),
        GeoPoint(-98.23597442933914, 17.92411146620965),
    ]),
    "Guerrero": Polygon([
        GeoPoint(-98.07862978825065, 16.0110296092669),
        GeoPoint(-97.54593323457897, 17.8415966116602),
        GeoPoint(-101.8761975763345, 19.2879448824476),
        GeoPoint(-102.5378210264313, 17.7258083999512),
        GeoPoint(-98.07862978825065, 16.0110296092669),
    ]),
    "Oaxaca": Polygon([
        GeoPoint(-94.06228754859151, 15.47721897238834),
        GeoPoint(-93.87265942984988, 18.35477333359784),
        GeoPoint(-98.59345543761631, 18.54701348538807),
        GeoPoint(-98.70231961564679, 15.62069465224437),
        GeoPoint(-94.06228754859151, 15.47721897238834),
    ]),
    "Michoacan": Polygon([
        GeoPoint(-100.3082496102006, 19.22258227299296),
        GeoPoint(-99.90574894221695, 20.25137939386669),
        GeoPoint(-101.7004679199828, 20.98750980416739),
        GeoPoint(-102.5163263850749, 20.04819533305848),
        GeoPoint(-100.3082496102006, 19.22258227299296),
    ]),
    "Colima": Polygon([
        GeoPoint(-102.1736180920661, 17.52391478191304),
        GeoPoint(-100.1106393437513, 19.34135457963665),
        GeoPoint(-103.1835224398227, 20.50015872501815),
        GeoPoint(-104.95654982688, 19.06711470238654),
        GeoPoint(-102.1736180920661, 17.52391478191304),
    ]),
    "Jalisco": Polygon([
        GeoPoint(-104.2491058523325, 18.38044565693096),
        GeoPoint(-101.3397552345668, 20.92694779732655),
        GeoPoint(-102.6629224869377, 22.03350792252786),
        GeoPoint(-106.3991102388304, 20.90634816402552),
        GeoPoint(-104.2491058523325, 18.38044565693096),
    ]),
    # TODO: Polygon 46 and 47 are incorrect
    "Puebla": Polygon([
        GeoPoint(-104.2491058523325, 18.38044565693096),
        GeoPoint(-101.3397552345668, 20.92694779732655),
        GeoPoint(-102.6629224869377, 22.03350792252786),
        GeoPoint(-106.3991102388304, 20.90634816402552),
        GeoPoint(-104.2491058523325, 18.38044565693096),
    ]),
    "Morelos": Polygon([
        GeoPoint(-104.2491058523325, 18.38044565693096),
        GeoPoint(-101.3397552345668, 20.92694779732655),
        GeoPoint(-102.6629224869377, 22.03350792252786),
        GeoPoint(-106.3991102388304, 20.90634816402552),
        GeoPoint(-104.2491058523325, 18.38044565693096),
    ]),
    "Veracruz": Polygon([
        GeoPoint(-93.25305668675571, 17.42108253392388),
        GeoPoint(-93.12916347987822, 18.52870348672094),
        GeoPoint(-97.73072782213934, 20.6891868605619),
        GeoPoint(-98.45648071083687, 18.1953653038331),
        GeoPoint(-93.25305668675571, 17.42108253392388),
    ]),
    "Chiapas": Polygon([
        GeoPoint(-93.27134825264807, 15.45412744189985),
        GeoPoint(-91.50417117489262, 16.99065334514076),
        GeoPoint(-94.04488228807821, 18.2991028252503),
        GeoPoint(-94.3660249339337, 16.12904295556978),
        GeoPoint(-93.27134825264807, 15.45412744189985),
    ])
}