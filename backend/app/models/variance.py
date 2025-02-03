from sqlmodel import Field, SQLModel, Relationship
from models.base_model import BaseModel

from typing import List

class Variance(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    name: str
    variance_type: str
    price: float
    product: "Product" = Relationship(back_populates="variances")
    basket_items: List["BasketItem"] = Relationship(back_populates="variance")