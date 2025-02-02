from sqlmodel import Session, SQLModel, select
from models.product import Product

from db.engine import DatabaseManager, get_session

from fastapi import APIRouter, Request, HTTPException, Depends

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/")
def get_all_products(session: Session = Depends(get_session)):
    statement = select(Product)
    products = session.exec(statement).all()

    products = [product.load_relations(relations_to_load=["variances"]) for product in products]

    session.close()

    return products

@router.get("/{product_id}")
def get_product_by_id(product_id: int, session: Session = Depends(get_session)):
    statement = select(Product).where(Product.id == product_id)
    product = session.exec(statement).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")

    product = product.load_relations(relations_to_load=["variances"])

    session.close()

    return product

@router.post("/")
async def create_product(request: Request, session: Session = Depends(get_session)):
    product_data = await request.json()

    base_price = product_data.get("base_price")
    name = product_data.get("name")
    furniture_type = product_data.get("furniture_type")
    product_type = product_data.get("product_type")
    height = product_data.get("height")
    width = product_data.get("width")
    depth = product_data.get("depth")

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

    new_product =new_product.load_relations(relations_to_load=["variances"])

    session.close()

    return new_product

@router.patch("/{product_id}")
async def update_product(product_id: int, request: Request, session: Session = Depends(get_session)):
    data = await request.json()

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

    product = product.load_relations(relations_to_load=["variances"])

    session.close()

    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")

    session.delete(product)
    session.commit()

    session.close()

    return {"message": "Product deleted successfully."}
