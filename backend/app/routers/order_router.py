from sqlmodel import Session, select
from models.user import User
from models.order import Order
from models.basket import Basket

from db.engine import DatabaseManager, get_session

from fastapi import APIRouter, Request, HTTPException, Depends, Query

NO_USER_DESCRIPTION = "The ID of the user whose basket is requested"

router = APIRouter(
    prefix="/order",
    tags=["order"],
)

@router.get("/")
def get_orders(session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    user = User.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    statement = (select(Order)
                 .join(Basket)
                 .where(Basket.user_id == user.id))

    orders = session.exec(statement).all()

    orders = [order.load_relations(["basket.basket_items.variance.product"]) for order in orders]

    session.close()

    return orders