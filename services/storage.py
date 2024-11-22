import json
from models.product import Product


class Storage:
    """Storage class. Saves products extracted from the webpage"""
    def __init__(self, db_path="db/scraped_data.json"):
        self.db_path = db_path

    def save_product(self, product: Product):
        data = self.load_data()
        data.append(product.model_dump())
        self.write_data(data)

    def load_data(self):
        try:
            with open(self.db_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def write_data(self, data):
        with open(self.db_path, "w") as file:
            json.dump(data, file, indent=4)
