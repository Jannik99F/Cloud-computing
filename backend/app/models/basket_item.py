from sqlmodel import Field, SQLModel, Relationship
from models.base_model import BaseModel

class BasketItem(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    variance_id: int = Field(foreign_key="variance.id")
    basket_id: int = Field(foreign_key="basket.id")
    amount: int
    base_price: float
    variance_price: float
    basket: "Basket" = Relationship(back_populates="basket_items")
    variance: "Variance" = Relationship(back_populates="basket_items")