from sqlmodel import Field, SQLModel, Relationship
from typing import List
from models.base_model import BaseModel

class User(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    password: str
    address: str
    baskets: List["Basket"] = Relationship(back_populates="user", cascade_delete=True)