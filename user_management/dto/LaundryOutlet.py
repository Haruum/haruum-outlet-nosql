from django.contrib.auth.hashers import make_password, check_password


class LaundryOutlet:
    def __init__(self):
        self.email = None
        self.name = None
        self.password = None
        self.phone_number = None

        self.address = None
        self.latitude = None
        self.longitude = None

        self.total_quota = 10
        self.amount_of_active_items = 0
        self.amount_of_reviewed_orders = 0
        self.is_available = True
        self.outlet_rating = 0

        self.items_provided = []

    def set_values_from_request(self, request_data, should_hash):
        self.email = request_data.get('email')
        self.name = request_data.get('name')
        self.phone_number = request_data.get('phone_number')
        self.address = request_data.get('address')
        self.latitude = request_data.get('latitude')
        self.longitude = request_data.get('longitude')

        if should_hash:
            self.password = make_password(request_data.get('password'))

        else:
            self.password = request_data.get('password')

    def set_values_from_query_result(self, result):
        self.set_values_from_request(result, should_hash=False)
        self.total_quota = result.get('total_quota')
        self.amount_of_active_items = result.get('amount_of_active_items')
        self.amount_of_reviewed_orders = result.get('amount_of_reviewed_orders')
        self.is_available = result.get('is_available')
        self.outlet_rating = result.get('outlet_rating')
        self.items_provided = result.get('items_provided')

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_name(self):
        return self.name

    def get_phone_number(self):
        return self.phone_number

    def get_address(self):
        return self.address

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_total_quota(self):
        return self.total_quota

    def get_amount_of_active_items(self):
        return self.amount_of_active_items

    def get_amount_of_reviewed_orders(self):
        return self.amount_of_reviewed_orders

    def get_is_available(self):
        return self.is_available

    def get_outlet_rating(self):
        return self.outlet_rating

    def get_items_provided(self):
        return self.items_provided

    def get_all(self):
        return {
            'email': self.get_email(),
            'name': self.get_name(),
            'phone_number': self.get_phone_number(),
            'password': self.get_password(),
            'address': self.get_address(),
            'latitude': self.get_latitude(),
            'longitude': self.get_longitude(),
            'total_quota': self.get_total_quota(),
            'amount_of_active_items': self.get_amount_of_active_items(),
            'amount_of_reviewed_orders': self.get_amount_of_reviewed_orders(),
            'is_available': self.get_is_available(),
            'outlet_rating': self.get_outlet_rating(),
            'items_provided': self.get_items_provided(),
        }

    def get_updatable_fields(self):
        return {
            'is_available': self.get_is_available(),
            'total_quota': self.get_total_quota(),
            'address': self.get_address(),
            'latitude': self.get_latitude(),
            'longitude': self.get_longitude(),
            'phone_number': self.get_phone_number()
        }

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_address(self, address):
        self.address = address

    def set_coordinate(self, coordinates):
        self.latitude = coordinates[0]
        self.longitude = coordinates[1]

    def set_is_available(self, is_available):
        self.is_available = is_available

    def set_quota(self, quota):
        self.total_quota = quota

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    def set_items_provided(self, items_provided):
        self.items_provided = items_provided
