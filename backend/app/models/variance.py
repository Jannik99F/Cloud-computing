from sqlmodel import Field, SQLModel, Relationship
from typing import Optional

class Variance(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    name: str
    variance_type: str
    price: float
    product: Optional["Product"] = Relationship(back_populates="variances")
