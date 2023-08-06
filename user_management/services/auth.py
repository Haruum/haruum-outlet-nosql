from django.core.exceptions import ObjectDoesNotExist

from haruum_outlet.decorators import catch_exception_and_convert_to_invalid_request_decorator
from haruum_outlet.exceptions import InvalidRegistrationException, InvalidRequestException
from haruum_outlet import utils as application_utils
from ..models import LaundryOutlet, ItemCategoryProvided
from . import utils
import numbers


def validate_basic_user_registration_data(request_data: dict):
    email = request_data.get('email').lower()
    password = request_data.get('password')

    if not email:
        raise InvalidRegistrationException('Email must not be null')

    if not utils.validate_email(email):
        raise InvalidRegistrationException('Email is invalid')

    if LaundryOutlet.objects.filter(email=email).exists():
        raise InvalidRegistrationException(f'Email {email} is already registered')

    if not password:
        raise InvalidRegistrationException('Password must not be null')

    validate_password_result = utils.validate_password(password)

    if not (validate_password_result['is_valid']):
        raise InvalidRegistrationException(validate_password_result['message'])

    if not isinstance(request_data.get('name'), str):
        raise InvalidRegistrationException('Name must be a string')

    if len(request_data.get('name')) > 100:
        raise InvalidRegistrationException('Name must not exceed 100 characters')


def validate_customer_does_not_exist_for_email(email):
    """
    This method fetches the CustomerService and
    checks if the inputted email exists in the customer's database.
    """


def validate_laundry_outlet_information(request_data: dict):
    if not request_data.get('phone_number'):
        raise InvalidRegistrationException('Phone number must not be null')

    if not isinstance(request_data.get('phone_number'), str):
        raise InvalidRegistrationException('Phone number must be a string')

    if not utils.validate_phone_number(request_data.get('phone_number')):
        raise InvalidRegistrationException('Phone number is invalid')

    if not request_data.get('address'):
        raise InvalidRegistrationException('Address must not be null')

    if not isinstance(request_data.get('address'), str):
        raise InvalidRegistrationException('Address must be a string')

    if not isinstance(request_data.get('latitude'), float):
        raise InvalidRegistrationException('Latitude must be a float')

    if not isinstance(request_data.get('longitude'), float):
        raise InvalidRegistrationException('Longitude must be a float')


def save_laundry_outlet_data(outlet_data: dict):
    email = outlet_data.get('email')
    password = outlet_data.get('password')
    name = outlet_data.get('name')
    phone_number = outlet_data.get('phone_number')
    address = outlet_data.get('address')
    latitude = outlet_data.get('latitude')
    longitude = outlet_data.get('longitude')

    laundry_outlet = LaundryOutlet.objects.create_user(
        email=email,
        password=password,
        name=name,
        phone_number=phone_number,
        address=address,
        latitude=latitude,
        longitude=longitude
    )

    return laundry_outlet


def validate_email_and_password(request_data: dict):
    email = request_data.get('email')
    password = request_data.get('password')

    if not isinstance(email, str):
        raise InvalidRequestException('Email must be a string')

    if not utils.validate_email(email):
        raise InvalidRequestException('Email is invalid')

    if not isinstance(password, str):
        raise InvalidRequestException('Password must be a string')


@catch_exception_and_convert_to_invalid_request_decorator((ObjectDoesNotExist,))
def check_email_and_password(request_data: dict):
    validate_email_and_password(request_data)
    laundry_outlet = utils.get_laundry_outlet_from_email(request_data.get('email'))
    return laundry_outlet.check_password(request_data.get('password'))


@catch_exception_and_convert_to_invalid_request_decorator((InvalidRegistrationException,))
def register_laundry_outlet(request_data: dict):
    validate_basic_user_registration_data(request_data)
    validate_customer_does_not_exist_for_email(request_data.get('email'))
    validate_laundry_outlet_information(request_data)
    laundry_outlet = save_laundry_outlet_data(request_data)
    return laundry_outlet


def get_laundry_outlet_data(request_data: dict):
    laundry_outlet = utils.get_laundry_outlet_from_email(request_data.get('email'))
    return laundry_outlet


def validate_update_availability_and_quota_data(request_data: dict):
    if not isinstance(request_data.get('is_available'), bool):
        raise InvalidRequestException('Availability status must be boolean')

    if not isinstance(request_data.get('quota'), int):
        raise InvalidRequestException('Quota must be an integer')


def save_updated_outlet_data(laundry_outlet: LaundryOutlet, request_data: dict):
    laundry_outlet.set_is_available(request_data.get('is_available'))
    laundry_outlet.set_quota(request_data.get('quota'))
    laundry_outlet.set_address(request_data.get('address'))
    laundry_outlet.set_coordinate([request_data.get('latitude'), request_data.get('longitude')])
    laundry_outlet.set_phone_number(request_data.get('phone_number'))


@catch_exception_and_convert_to_invalid_request_decorator((InvalidRegistrationException, ObjectDoesNotExist))
def update_outlet_data(request_data: dict):
    validate_update_availability_and_quota_data(request_data)
    validate_laundry_outlet_information(request_data)
    laundry_outlet = utils.get_laundry_outlet_from_email(request_data.get('email'))
    save_updated_outlet_data(laundry_outlet, request_data)


def validate_service_category_datum(service_category_data):
    if not application_utils.is_uuid(service_category_data.get('service_category_id')):
        raise InvalidRequestException('Service category ID must be a UUID string')

    if not utils.predetermined_service_category_exists(service_category_data.get('service_category_id')):
        raise InvalidRequestException('Service category ID does not exist')

    if not isinstance(service_category_data.get('price_per_item'), numbers.Number):
        raise InvalidRequestException('Price per item must be of type float')


def validate_update_item_category_data(request_data):
    if not utils.laundry_outlet_with_email_exist(request_data.get('email')):
        raise InvalidRequestException('Laundry Outlet with email does not exist')

    if not isinstance(request_data.get('services_provided'), list):
        raise InvalidRequestException('Service Provided must be a list')

    for service_provided in request_data.get('services_provided'):
        validate_service_category_datum(service_provided)


def update_existing_or_create_services_data(laundry_outlet_email: str, services_provided: list):
    outlet_provided_services = ItemCategoryProvided.objects.filter(laundry_outlet_email=laundry_outlet_email)

    for service_provided in services_provided:
        service_category_id = service_provided.get('service_category_id')
        item_price = service_provided.get('price_per_item')
        matching_provided_services = outlet_provided_services.filter(service_category_id=service_category_id)

        if len(matching_provided_services) > 0:
            matching_provided_service = matching_provided_services[0]
            matching_provided_service.set_item_price(item_price)

        else:
            ItemCategoryProvided.objects.create(
                laundry_outlet_email=laundry_outlet_email,
                service_category_id=service_category_id,
                item_price=item_price
            )


def update_item_category_provided(request_data: dict):
    validate_update_item_category_data(request_data)
    update_existing_or_create_services_data(
        request_data.get('email'),
        request_data.get('services_provided')
    )









