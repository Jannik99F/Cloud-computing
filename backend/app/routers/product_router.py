from sqlmodel import Session, SQLModel, select
from models.product import Product

from db.engine import DatabaseManager

from fastapi import APIRouter, Request, HTTPException

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/")
def get_all_products():
    with DatabaseManager.get_session() as session:
        statement = select(Product)
        products = session.exec(statement).all()

    return {"products": products}

@router.get("/{product_id}")
def get_product_by_id(product_id: int):
    with DatabaseManager.get_session() as session:
        statement = select(Product).where(Product.id == product_id)
        product = session.exec(statement).first()

        if product is None:
            raise HTTPException(status_code=404, detail="Product not found.")

    return {"product": product}

@router.post("/")
async def create_product(request: Request):
    product_data = await request.json()

    base_price = product_data.get("base_price")
    name = product_data.get("name")
    furniture_type = product_data.get("furniture_type")
    product_type = product_data.get("product_type")
    height = product_data.get("height")
    width = product_data.get("width")
    depth = product_data.get("depth")

    with DatabaseManager.get_session() as session:
        new_product = Product(
            base_price=base_price,
            name=name,
            furniture_type=furniture_type,
            product_type=product_type,
            height=height,
            width=width,
            depth=depth,
        )
        session.add(new_product)
        session.commit()

        session.refresh(new_product)

    return {"product": new_product.dict()}

@router.patch("/{product_id}")
async def update_product(product_id: int, request: Request):
    data = await request.json()

    with DatabaseManager.get_session() as session:
        statement = select(Product).where(Product.id == product_id)
        product = session.exec(statement).first()

        if product is None:
            raise HTTPException(status_code=404, detail="Product not found.")

        for key, value in data.items():
            if value is not None and hasattr(product, key):
                setattr(product, key, value)

        session.add(product)
        session.commit()

        session.refresh(product)

    return {"product": product.dict()}

@router.delete("/{product_id}")
def delete_product(product_id: int):
    with DatabaseManager.get_session() as session:
        product = session.get(Product, product_id)

        if product is None:
            raise HTTPException(status_code=404, detail="Product not found.")

        session.delete(product)
        session.commit()

    return {"message": "Product deleted successfully."}
