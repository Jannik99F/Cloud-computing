from sqlmodel import Field, SQLModel, Relationship
from models.base_model import BaseModel

class Basket(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="baskets")
