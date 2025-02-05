from sqlmodel import Field, SQLModel, Relationship
from models.base_model import BaseModel
from typing import Optional

class BasketItem(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    variance_id: int = Field(foreign_key="variance.id")
    basket_id: int = Field(foreign_key="basket.id", ondelete="CASCADE")
    amount: int
    base_price: Optional[float] = Field(default=None, nullable=True)
    variance_price: Optional[float] = Field(default=None, nullable=True)
    basket: "Basket" = Relationship(back_populates="basket_items")
    variance: "Variance" = Relationship(back_populates="basket_items")