from rss.cap.geopoint import GeoPoint

STATES = {
    40: 'CDMX',
    41: 'Guerrero',
    42: 'Oaxaca',
    43: 'Michoacan',
    44: 'Colima',
    45: 'Jalisco',
    46: 'Puebla',
    47: 'Morelos',
    48: 'Veracruz',
    49: 'Chiapas',
}

STATES_COORDS = {
    'CDMX': GeoPoint(lat=19.42847, lon=-99.12766),
    'Guerrero': GeoPoint(lat=17.4392, lon=-99.5451),
    'Oaxaca': GeoPoint(lat=17.0732, lon=-96.7266),
    'Michoacán': GeoPoint(lat=19.5665, lon=-101.7068),
    'Colima': GeoPoint(lat=19.2452, lon=-103.7241),
    'Jalisco': GeoPoint(lat=20.6595, lon=-103.3494),
    'Puebla': GeoPoint(lat=19.0414, lon=-98.2063),
    'Morelos': GeoPoint(lat=18.6813, lon=-99.1013),
    'Veracruz': GeoPoint(lat=19.1738, lon=-96.1342),
    'Chiapas': GeoPoint(lat=16.7569, lon=-93.1292),
}
