from haruum_outlet import utils as application_utils
from haruum_outlet.exceptions import InvalidRequestException
from user_management.models import (
    LaundryOutlet,
    ItemCategoryProvided,
    PredeterminedServiceCategory
)
from user_management.services import utils as user_management_utils


def get_outlets_based_on_name(outlet_name):
    if outlet_name is not None:
        laundry_outlets = LaundryOutlet.objects.filter(name__icontains=outlet_name)
    else:
        laundry_outlets = LaundryOutlet.objects.all()

    return laundry_outlets


def sort_laundry_outlet_based_on_distance_to_coordinate(laundry_outlets, latitude, longitude):
    """
    This function sorts the laundry outlet based on distance to coordinate.
    """
    return []


def get_outlets(request_data):
    laundry_outlets = get_outlets_based_on_name(request_data.get('name'))
    latitude = application_utils.save_convert_string_to_number(request_data.get('latitude'))
    longitude = application_utils.save_convert_string_to_number(request_data.get('longitude'))

    if latitude is not None and longitude is not None:
        laundry_outlets = sort_laundry_outlet_based_on_distance_to_coordinate(
            laundry_outlets=laundry_outlets,
            latitude=latitude,
            longitude=longitude
        )

    return laundry_outlets


def validate_outlet_provided_services_request(request_data):
    if not user_management_utils.laundry_outlet_with_email_exist(request_data.get('email')):
        raise InvalidRequestException('Laundry Outlet with email does not exist')


def get_outlet_provided_services(request_data):
    validate_outlet_provided_services_request(request_data)
    provided_services = ItemCategoryProvided.objects.filter(laundry_outlet_email=request_data.get('email'))
    return provided_services


def get_predetermined_service_categories():
    return PredeterminedServiceCategory.objects.all()









