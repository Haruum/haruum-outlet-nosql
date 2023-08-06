from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from typing import Optional, Dict
import numbers
import uuid


def is_uuid(uuid_string) -> bool:
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False


def get_coordinate_pair_of_address(address) -> Optional[Dict]:
    geolocator = Nominatim(user_agent="https://nominatim.org")

    try:
        location = geolocator.geocode(address)
        if location is not None:
            return {
                'latitude': location.latitude,
                'longitude': location.longitude
            }

    except GeocoderUnavailable:
        return None


def save_convert_string_to_number(number_string) -> Optional[float]:
    try:
        return float(number_string)

    except TypeError:
        return None
