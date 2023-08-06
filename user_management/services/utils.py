from django.core.exceptions import ObjectDoesNotExist
from typing import Optional, Match
from ..models import LaundryOutlet, PredeterminedServiceCategory
import phonenumbers
import uuid
import re

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def validate_email(email) -> Optional[Match[str]]:
    return re.fullmatch(email_regex, email)


def validate_password(password) -> dict:
    validation_result = {
        'is_valid': True,
        'message': None
    }

    if len(password) < 8:
        validation_result['is_valid'] = False
        validation_result['message'] = 'Password length must be at least 8 characters'

    elif not any(character.isupper() for character in password):
        validation_result['is_valid'] = False
        validation_result['message'] = 'Password must contain at least 1 uppercase character'

    elif not any(character.islower() for character in password):
        validation_result['is_valid'] = False
        validation_result['message'] = 'Password must contain at least 1 lowercase character'

    elif not any(character.isdigit() for character in password):
        validation_result['is_valid'] = False
        validation_result['message'] = 'Password must contain at least 1 number character'

    return validation_result


def validate_phone_number(phone_number_string) -> bool:
    try:
        phone_number = phonenumbers.parse(phone_number_string)
        return phonenumbers.is_valid_number(phone_number)

    except phonenumbers.NumberParseException:
        return False


def get_laundry_outlet_from_email(email) -> LaundryOutlet:
    found_outlet = LaundryOutlet.objects.filter(email=email)

    if found_outlet:
        return found_outlet[0]
    else:
        raise ObjectDoesNotExist(f'Laundry Outlet with email {email} does not exist')


def get_laundry_outlet_from_email_thread_safe(email) -> LaundryOutlet:
    found_outlet = LaundryOutlet.objects.filter(email=email).select_for_update()

    if found_outlet:
        return found_outlet[0]
    else:
        raise ObjectDoesNotExist(f'Laundry Outlet with email {email} does not exist')


def laundry_outlet_with_email_exist(email) -> bool:
    return LaundryOutlet.objects.filter(email=email).exists()


def predetermined_service_category_exists(service_category_id) -> bool:
    return PredeterminedServiceCategory.objects.filter(id=uuid.UUID(service_category_id)).exists()
