from typing import Optional, Match
from ..dto.LaundryOutlet import LaundryOutlet
from ..dto.ItemCategoryProvided import ItemCategoryProvided
import phonenumbers
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


def get_outlet_provided_services(outlet: LaundryOutlet):
    return [
        ItemCategoryProvided(
            item_id=item.get('id'),
            item_name=item.get('service_category_name'),
            item_price=item.get('item_price')
        ) for item in outlet.get_items_provided()
    ]
