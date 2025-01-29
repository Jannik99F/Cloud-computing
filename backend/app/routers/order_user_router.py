from sqlmodel import Session, SQLModel, select
from models.user import User
from models.variance import Variance
from models.basket_item import BasketItem

from db.engine import DatabaseManager, get_session

from fastapi import APIRouter, Request, HTTPException, Depends, Query

router = APIRouter(
    prefix="/current-order",
    tags=["order"],
)

@router.put("/")
def get_current_order(session: Session = Depends(get_session), user_id: int = Query(..., description="The ID of the user whose basket is requested")):
    user = User.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user.get_current_order(session).load_relations(["basket.basket_items.variance.product"])