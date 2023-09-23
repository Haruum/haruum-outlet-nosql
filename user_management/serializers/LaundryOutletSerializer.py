class LaundryOutletSerializer:
    def __init__(self, outlet_dto, many=False):
        if many:
            self.data = [LaundryOutletSerializer._serialize(outlet) for outlet in outlet_dto]

        else:
            self.data = LaundryOutletSerializer._serialize(outlet_dto)

    @staticmethod
    def _serialize(outlet_dto):
        return {
            'email': outlet_dto.get_email(),
            'name': outlet_dto.get_name(),
            'phone_number': outlet_dto.get_phone_number(),
            'address': outlet_dto.get_address(),
            'total_quota': outlet_dto.get_total_quota(),
            'amount_of_active_items': outlet_dto.get_amount_of_active_items(),
            'is_available': outlet_dto.get_is_available(),
            'outlet_rating': outlet_dto.get_outlet_rating(),
            'items_provided': outlet_dto.get_items_provided(),
        }
