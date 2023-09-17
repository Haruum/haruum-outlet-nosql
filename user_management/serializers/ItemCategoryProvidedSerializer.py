class ItemCategoryProvidedSerializer:
    def __init__(self, item_category_provided, many=False):
        if many:
            self.data = [item.get_all() for item in item_category_provided]

        else:
            self.data = item_category_provided.get_all()

