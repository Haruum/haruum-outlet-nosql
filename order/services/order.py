from haruum_outlet.exceptions import InvalidRequestException
from user_management.services import utils as user_management_utils


def register_order_to_outlet(request_data):
    laundry_outlet_email = request_data.get('laundry_outlet_email')
    laundry_outlet = user_management_utils.get_laundry_outlet_from_email_thread_safe(laundry_outlet_email)
    laundry_outlet.accept_one_order()


def finish_order_from_outlet(request_data):
    laundry_outlet_email = request_data.get('laundry_outlet_email')
    laundry_outlet = user_management_utils.get_laundry_outlet_from_email_thread_safe(laundry_outlet_email)
    laundry_outlet.finish_one_order()


def validate_rating_data(request_data):
    if not isinstance(request_data.get('new_rating'), int):
        raise InvalidRequestException('New rating should be an integer')


def update_outlet_rating(request_data):
    validate_rating_data(request_data)
    laundry_outlet = user_management_utils.get_laundry_outlet_from_email_thread_safe(
        request_data.get('laundry_outlet_email')
    )
    laundry_outlet.recompute_outlet_rating(request_data.get('new_rating'))


