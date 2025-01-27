from sqlmodel import Session, SQLModel, select
from models.variance import Variance
from models.product import Product

from db.engine import DatabaseManager

from fastapi import APIRouter, Request, HTTPException

router = APIRouter(
    prefix="/variances",
    tags=["variances"]
)

@router.get("/")
def get_all_variances():
    with DatabaseManager.get_session() as session:
        statement = select(Variance)
        variances = session.exec(statement).all()

    return {"variances": variances}

@router.get("/{variance_id}")
def get_variance_by_id(variance_id: int):
    with DatabaseManager.get_session() as session:
        statement = select(Variance).where(Variance.id == variance_id)
        variance = session.exec(statement).first()

        if variance is None:
            raise HTTPException(status_code=404, detail="Variance not found.")

    return {"variance": variance}

@router.post("/")
async def create_variance(request: Request):
    user_data = await request.json()

    product_id = user_data.get("product_id")
    name = user_data.get("name")
    variance_type = user_data.get("variance_type")
    price = user_data.get("price")

    with DatabaseManager.get_session() as session:
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

    return {"variance": new_variance.dict()}

@router.patch("/{variance_id}")
async def update_variance(variance_id: int, request: Request):
    data = await request.json()

    with DatabaseManager.get_session() as session:
        statement = select(Variance).where(Variance.id == variance_id)
        variance = session.exec(statement).first()

        if variance is None:
            raise HTTPException(status_code=404, detail="Variance not found.")

        if "product_id" in data:
            raise HTTPException(status_code=400, detail="product_id cannot be updated.")

        for key, value in data.items():
            if value is not None and hasattr(variance, key):
                setattr(variance, key, value)

        session.add(variance)
        session.commit()

        session.refresh(variance)

    return {"variance": variance.dict()}



@router.delete("/{variance_id}")
def delete_user(variance_id: int):
    with DatabaseManager.get_session() as session:
        variance = session.get(Variance, variance_id)

        if variance is None:
            raise HTTPException(status_code=404, detail="Variance not found.")

        session.delete(variance)
        session.commit()

    return {"message": "Variance deleted successfully."}
