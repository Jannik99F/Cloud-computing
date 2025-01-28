from sqlmodel import Session, SQLModel, select
from models.variance import Variance
from models.product import Product

from db.engine import DatabaseManager, get_session

from fastapi import APIRouter, Request, HTTPException, Depends


def check_product_exists(product_id: int):
    statement = select(Product).where(Product.id == product_id)
    product = get_session().exec(statement).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")

router = APIRouter(
    prefix="/products/{product_id}/variances",
    tags=["variances"],
    dependencies=[Depends(check_product_exists)],
)

@router.get("/")
def get_all_variances(product_id, session: Session = Depends(get_session)):
    statement = select(Variance).where(Variance.product_id == product_id)
    variances = session.exec(statement).all()

    return variances

@router.get("/{variance_id}")
def get_variance_by_id(variance_id: int, session: Session = Depends(get_session)):
    statement = select(Variance).where(Variance.id == variance_id)
    variance = session.exec(statement).first()

    if variance is None:
        raise HTTPException(status_code=404, detail="Variance not found.")

    return variance

@router.post("/")
async def create_variance(product_id: int, request: Request, session: Session = Depends(get_session)):
    user_data = await request.json()

    name = user_data.get("name")
    variance_type = user_data.get("variance_type")
    price = user_data.get("price")

    product_exists = session.exec(select(Product).where(Product.id == product_id)).first()

    if not product_exists:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found.")

    new_variance = Variance(
        product_id=product_id,
        name=name,
        variance_type=variance_type,
        price=price,
    )
    session.add(new_variance)
    session.commit()

    session.refresh(new_variance)

    return new_variance

@router.patch("/{variance_id}")
async def update_variance(variance_id: int, request: Request, session: Session = Depends(get_session)):
    data = await request.json()

    statement = select(Variance).where(Variance.id == variance_id)
    variance = session.exec(statement).first()

    if variance is None:
        raise HTTPException(status_code=404, detail="Variance not found.")

    for key, value in data.items():
        if value is not None and hasattr(variance, key):
            setattr(variance, key, value)

    session.add(variance)
    session.commit()

    session.refresh(variance)

    return variance



@router.delete("/{variance_id}")
def delete_user(variance_id: int, session: Session = Depends(get_session)):
    variance = session.get(Variance, variance_id)

    if variance is None:
        raise HTTPException(status_code=404, detail="Variance not found.")

    session.delete(variance)
    session.commit()

    return {"message": "Variance deleted successfully."}