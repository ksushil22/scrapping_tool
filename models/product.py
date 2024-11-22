from pydantic import BaseModel


class Product(BaseModel):
    """Product model for saving the title, price and path to image"""
    product_title: str
    product_price: float
    path_to_image: str
