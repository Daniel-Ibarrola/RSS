from dataclasses import dataclass
import math


@dataclass(frozen=True)
class GeoPoint:
    lon: float
    lat: float


def distance_between_points(point1: GeoPoint, point2: GeoPoint) -> float:
    lat1, lon1 = math.radians(point1.lat), math.radians(point2.lon)
    lat2, lon2 = math.radians(point2.lat), math.radians(point2.lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    earth_radius = 6371  # in Km
    # Angular separation
    sep = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    angular_distance = 2 * math.atan2(math.sqrt(sep), math.sqrt(1 - sep))
    return earth_radius * angular_distance  # Earth's mean radius in kilometers
