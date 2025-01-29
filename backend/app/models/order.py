from sqlmodel import Field, SQLModel, Relationship
from models.base_model import BaseModel
from typing import Optional

class Order(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    shipping_address: Optional["str"]
    billing_address: Optional["str"]
    payment_method: Optional["str"]
    payed: bool
    status: str
    basket_id: int = Field(default=None, foreign_key="basket.id")
    basket: "Basket" = Relationship(back_populates="order")