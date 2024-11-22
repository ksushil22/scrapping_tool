class Cache:
    """
    A simple class to make sure no product with same title and price is repeated.
    """
    def __init__(self):
        self.cache = {}

    def is_cached(self, product):
        key = product.product_title
        if key in self.cache and self.cache[key] == product.product_price:
            return True
        return False

    def add_to_cache(self, product):
        self.cache[product.product_title] = product.product_price
