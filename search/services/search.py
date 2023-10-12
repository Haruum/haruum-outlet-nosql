from . import utils
from django.core.exceptions import ObjectDoesNotExist
from haruum_outlet import utils as application_utils
from haruum_outlet.decorators import catch_exception_and_convert_to_invalid_request_decorator
from user_management.repositories import outlet as outlet_repository


def sort_laundry_outlet_based_on_distance_to_coordinate(laundry_outlets, latitude, longitude):
    """
    This function sorts the laundry outlet based on distance to coordinate.
    """
    return sorted(
        laundry_outlets,
        key=lambda outlet: utils.haversine(
            outlet.get_latitude(),
            outlet.get_longitude(),
            latitude, longitude
        )
    )


def get_outlets(request_data):
    laundry_outlets = outlet_repository.get_outlets(name=request_data.get('name'))
    latitude = application_utils.save_convert_string_to_number(request_data.get('latitude'))
    longitude = application_utils.save_convert_string_to_number(request_data.get('longitude'))

    if latitude is not None and longitude is not None:
        laundry_outlets = sort_laundry_outlet_based_on_distance_to_coordinate(
            laundry_outlets=laundry_outlets,
            latitude=latitude,
            longitude=longitude
        )

    return laundry_outlets


@catch_exception_and_convert_to_invalid_request_decorator((ObjectDoesNotExist,))
def get_outlet_provided_services(request_data):
    laundry_outlet = outlet_repository.get_outlet_by_email(request_data.get('email'))
    return laundry_outlet.get_items_provided()










