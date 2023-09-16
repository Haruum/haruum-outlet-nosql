from django.core.exceptions import ObjectDoesNotExist
from haruum_outlet.settings import DATABASE
from haruum_outlet.collections import OUTLET
from ..dto.LaundryOutlet import LaundryOutlet
import re


def get_outlet_by_email(email):
    found_outlet = DATABASE[OUTLET].find_one({'email': email})

    if found_outlet is not None:
        outlet = LaundryOutlet()
        outlet.set_values_from_query_result(found_outlet)
        return outlet

    else:
        raise ObjectDoesNotExist(f'Laundry Outlet with email {email} does not exist')


def outlet_with_email_exists(email):
    try:
        get_outlet_by_email(email)
        return True

    except ObjectDoesNotExist:
        return False


def get_outlets(name=None):
    if name is not None:
        found_outlets = DATABASE[OUTLET].find({'name': re.compile(name, re.IGNORECASE)})
    else:
        found_outlets = DATABASE[OUTLET].find()

    converted_outlets = []
    for outlet_data in found_outlets:
        outlet = LaundryOutlet()
        outlet.set_values_from_query_result(outlet_data)
        converted_outlets.append(outlet)

    return converted_outlets


def create_outlet(laundry_dto: LaundryOutlet, database_session):
    DATABASE[OUTLET].insert_one(laundry_dto.get_all(), session=database_session)
    return laundry_dto


def update_outlet(laundry_dto: LaundryOutlet, database_session):
    DATABASE[OUTLET].update_one(
        {'email': laundry_dto.get_email()},
        {'$set': laundry_dto.get_updatable_fields()},
        session=database_session
    )


def update_outlet_services(outlet_email: str, items_provided, database_session):
    DATABASE[OUTLET].update_one(
        {'email': outlet_email},
        {'$set': {
            'items_provided': items_provided
        }},
        session=database_session
    )
