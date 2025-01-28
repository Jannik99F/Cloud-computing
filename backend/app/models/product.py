from sqlmodel import Field, SQLModel, Relationship
from typing import List
from models.base_model import BaseModel

class Product(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    base_price: float
    name: str
    furniture_type: str
    product_type: str
    height: float
    width: float
    depth: float
    variances: List["Variance"] = Relationship(back_populates="product", cascade_delete=True)
