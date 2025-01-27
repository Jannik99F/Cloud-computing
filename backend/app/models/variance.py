from sqlmodel import Field, SQLModel

class Variance(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    name: str
    variance_type: str
    price: float