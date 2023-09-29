from django.core.exceptions import ObjectDoesNotExist
from haruum_outlet.decorators import catch_exception_and_convert_to_invalid_request_decorator
from haruum_outlet.exceptions import (
    InvalidRegistrationException,
    InvalidRequestException,
)
from ..repositories import outlet as outlet_repository
from ..dto.LaundryOutlet import LaundryOutlet
from ..dto.ItemCategoryProvided import ItemCategoryProvided
from . import utils
import numbers

from ..serializers.ItemCategoryProvidedSerializer import ItemCategoryProvidedSerializer


def validate_basic_user_registration_data(request_data: dict):
    email = request_data.get('email').lower()
    password = request_data.get('password')

    if not email:
        raise InvalidRegistrationException('Email must not be null')

    if not utils.validate_email(email):
        raise InvalidRegistrationException('Email is invalid')

    if outlet_repository.outlet_with_email_exists(email):
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


def validate_laundry_outlet_information(request_data: dict):
    if not request_data.get('phone_number'):
        raise InvalidRegistrationException('Phone number must not be null')

    if not isinstance(request_data.get('phone_number'), str):
        raise InvalidRegistrationException('Phone number must be a string')

    if len(request_data.get('phone_number')) > 15:
        raise InvalidRegistrationException('Phone number must not exceed 15 characters')

    if not utils.validate_phone_number(request_data.get('phone_number')):
        raise InvalidRegistrationException('Phone number is invalid')

    if not request_data.get('address'):
        raise InvalidRegistrationException('Address must not be null')

    if not isinstance(request_data.get('address'), str):
        raise InvalidRegistrationException('Address must be a string')

    if not isinstance(request_data.get('latitude'), numbers.Number):
        raise InvalidRegistrationException('Latitude must be a number')

    if not isinstance(request_data.get('longitude'), numbers.Number):
        raise InvalidRegistrationException('Longitude must be a number')


def save_laundry_outlet_data(outlet_data: dict):
    laundry_outlet = LaundryOutlet()
    laundry_outlet.set_values_from_request(outlet_data, should_hash=True)
    return outlet_repository.create_outlet(laundry_outlet)


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
    laundry_outlet = outlet_repository.get_outlet_by_email(request_data.get('email'))
    return laundry_outlet.check_password(request_data.get('password'))


@catch_exception_and_convert_to_invalid_request_decorator((InvalidRegistrationException,))
def register_laundry_outlet(request_data: dict):
    validate_basic_user_registration_data(request_data)
    validate_laundry_outlet_information(request_data)
    laundry_outlet = save_laundry_outlet_data(request_data)
    return laundry_outlet


@catch_exception_and_convert_to_invalid_request_decorator((ObjectDoesNotExist,))
def get_laundry_outlet_data(request_data: dict):
    laundry_outlet = outlet_repository.get_outlet_by_email(request_data.get('email'))
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
    outlet_repository.update_outlet(laundry_outlet)


@catch_exception_and_convert_to_invalid_request_decorator((InvalidRegistrationException, ObjectDoesNotExist))
def update_outlet_data(request_data: dict):
    validate_update_availability_and_quota_data(request_data)
    validate_laundry_outlet_information(request_data)
    laundry_outlet = outlet_repository.get_outlet_by_email(request_data.get('email'))
    save_updated_outlet_data(laundry_outlet, request_data)


def validate_service_category_datum(service_category_data):
    if not isinstance(service_category_data.get('service_category_name'), str):
        raise InvalidRequestException('Service category name must be a string')

    if not isinstance(service_category_data.get('price_per_item'), numbers.Number):
        raise InvalidRequestException('Price per item must be of type number')

    if service_category_data.get('price_per_item') <= 0:
        raise InvalidRequestException('Price per item must be a positive number')


def validate_update_item_category_data(request_data):
    if not isinstance(request_data.get('services_provided'), list):
        raise InvalidRequestException('Service Provided must be a list')

    for service_provided in request_data.get('services_provided'):
        validate_service_category_datum(service_provided)


def update_existing_or_create_services_data(laundry_outlet: LaundryOutlet, updated_services_provided: list):
    outlet_provided_services = utils.get_outlet_provided_services(laundry_outlet)

    for service_provided in updated_services_provided:
        service_category_name = service_provided.get("service_category_name").strip().lower()
        item_price = service_provided.get("price_per_item")
        matching_provided_services = [
            item
            for item in outlet_provided_services
            if item.get_name() == service_category_name
        ]

        if len(matching_provided_services) > 0:
            matching_provided_service = matching_provided_services[0]
            matching_provided_service.set_item_price(item_price)

        else:
            outlet_provided_services.append(
                ItemCategoryProvided(
                    item_name=service_category_name,
                    item_price=item_price
                )
            )

    outlet_repository.update_outlet_services(
        laundry_outlet.get_email(),
        ItemCategoryProvidedSerializer(outlet_provided_services, many=True).data
    )


@catch_exception_and_convert_to_invalid_request_decorator((ObjectDoesNotExist,))
def update_item_category_provided(request_data: dict):
    laundry_outlet = outlet_repository.get_outlet_by_email(request_data.get('email'))
    validate_update_item_category_data(request_data)
    update_existing_or_create_services_data(
        laundry_outlet,
        request_data.get('services_provided')
    )


def check_outlet_existence(request_data):
    return outlet_repository.outlet_with_email_exists(request_data.get('email'))
