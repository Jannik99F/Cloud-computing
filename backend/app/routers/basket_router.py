from sqlmodel import Session, SQLModel, select
from models.basket import Basket

from db.engine import DatabaseManager, get_session

from fastapi import APIRouter, Request, HTTPException, Depends

router = APIRouter(
    prefix="/baskets",
    tags=["baskets"]
)

@router.get("/{basket_id}")
def get_basket_by_id(basket_id: int, session: Session = Depends(get_session)):
    statement = select(Basket).where(Basket.id == basket_id)
    basket = session.exec(statement).first()

    if basket is None:
        raise HTTPException(status_code=404, detail="Basket not found.")

    return basket

@router.post("/")
async def create_product(request: Request, session: Session = Depends(get_session)):
    product_data = await request.json()

    user_id = product_data.get("user_id")

    new_basket = Basket(
        user_id=user_id,
    )
    session.add(new_basket)
    session.commit()

    session.refresh(new_basket)

    return new_basket
