from haruum_outlet.exceptions import MatchedNoRecordException
from haruum_outlet.settings import DATABASE
from haruum_outlet.collections import OUTLET
from user_management.dto.LaundryOutlet import LaundryOutlet


def update_accept_one_order(outlet_email, order_quantity):
    update_result = DATABASE[OUTLET].update_one(
        {
            'email': outlet_email,
            '$expr': {
                '$lte': [
                    {'$add': ['$amount_of_active_items', order_quantity]},
                    '$total_quota'
                ]
            }
        },
        {'$inc': {'amount_of_active_items': order_quantity}}
    )

    if update_result.matched_count == 0:
        raise MatchedNoRecordException('Update condition does not match any record')


def update_finish_one_order(outlet_email, order_quantity):
    update_result = DATABASE[OUTLET].update_one(
        {
            'email': outlet_email,
            '$expr': {
              '$gte': ['$amount_of_active_items', order_quantity]
            },
        },
        {'$inc': {'amount_of_active_items': -order_quantity}}
    )

    if update_result.matched_count == 0:
        raise MatchedNoRecordException('Update condition does not match any record')


def update_outlet_rating(outlet_email, new_rating: int):
    DATABASE['outlet'].update_one(
        {'email': outlet_email},
        [
            {'$set': {
                'previous_accumulative_rating': {
                    '$multiply': ['$outlet_rating', '$amount_of_reviewed_orders']
                }
            }},
            {
                '$set': {
                    'new_accumulative_rating': {
                        '$add': ['$previous_accumulative_rating', new_rating]
                    }
                }
            },
            {
                '$set': {
                    'amount_of_reviewed_orders': {
                        '$add': ['$amount_of_reviewed_orders', 1]
                    }
                }
            },
            {
                '$set': {
                    'outlet_rating': {
                        '$divide': ['$new_accumulative_rating', '$amount_of_reviewed_orders']
                    }
                }
            },
            {
                '$unset': ['previous_accumulative_rating', 'new_accumulative_rating']
            }
        ]
    )
