import uuid


class ItemCategoryProvided:
    def __init__(self, item_name, item_price, item_id=None):
        self.id = item_id if item_id is not None else uuid.uuid4()
        self.name = item_name
        self.item_price = item_price

    def get_name(self):
        return self.name

    def set_item_price(self, item_price):
        self.item_price = item_price

    def get_all(self):
        return {
            'id': str(self.id),
            'service_category_name': self.name,
            'item_price': self.item_price
        }


