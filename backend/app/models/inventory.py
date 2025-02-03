from sqlmodel import Field, SQLModel, Relationship
from models.base_model import BaseModel

class Inventory(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    variance_id: int = Field(foreign_key="variance.id", unique=True)
    amount: int
    variance: "Variance" = Relationship(back_populates="inventory")