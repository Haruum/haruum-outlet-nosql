from django.core.exceptions import ObjectDoesNotExist
from haruum_outlet.decorators import catch_exception_and_convert_to_invalid_request_decorator
from haruum_outlet.exceptions import InvalidRequestException, MatchedNoRecordException
from user_management.repositories import outlet as outlet_repository
from ..exceptions import OrderException
from ..repositories import order as order_repository


def validate_order_quantity_in_request(request_data):
    if not isinstance(request_data.get('order_quantity'), int):
        raise InvalidRequestException('Order quantity must be an integer')

    if request_data.get('order_quantity') <= 0:
        raise InvalidRequestException('Order quantity must be positive')


def validate_accept_order_request(laundry_outlet):
    if not laundry_outlet.get_is_available():
        raise OrderException(f'Laundry outlet {laundry_outlet.get_name()} is currently not accepting order')


@catch_exception_and_convert_to_invalid_request_decorator((OrderException, ObjectDoesNotExist))
def register_order_to_outlet(request_data):
    validate_order_quantity_in_request(request_data)
    laundry_outlet = outlet_repository.get_outlet_by_email(request_data.get('laundry_outlet_email'))
    validate_accept_order_request(laundry_outlet)

    try:
        order_repository.update_accept_one_order(
            laundry_outlet.get_email(),
            request_data.get('order_quantity')
        )
    except MatchedNoRecordException:
        raise OrderException(f'Laundry outlet {laundry_outlet.get_name()} has reached its maximum workload')


@catch_exception_and_convert_to_invalid_request_decorator((OrderException, ObjectDoesNotExist))
def finish_order_from_outlet(request_data):
    validate_order_quantity_in_request(request_data)
    laundry_outlet_email = request_data.get('laundry_outlet_email')
    laundry_outlet = outlet_repository.get_outlet_by_email(laundry_outlet_email)

    try:
        order_repository.update_finish_one_order(
            laundry_outlet.get_email(),
            request_data.get('order_quantity')
        )
    except MatchedNoRecordException:
        raise OrderException(
            f'Laundry outlet {laundry_outlet.get_name()} has less orders than {request_data.get("order_quantity")}'
        )


def validate_rating_data(request_data):
    if not isinstance(request_data.get('new_rating'), int):
        raise InvalidRequestException('New rating should be an integer')


@catch_exception_and_convert_to_invalid_request_decorator((ObjectDoesNotExist,))
def update_outlet_rating(request_data):
    validate_rating_data(request_data)
    laundry_outlet = outlet_repository.get_outlet_by_email(request_data.get('laundry_outlet_email'))
    order_repository.update_outlet_rating(
        laundry_outlet.get_email(),
        request_data.get('new_rating')
    )



