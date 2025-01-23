from sqlmodel import Field, SQLModel

class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    base_price: float
    name: str
    furniture_type: str
    product_type: str
    height: float
    width: float
    depth: float