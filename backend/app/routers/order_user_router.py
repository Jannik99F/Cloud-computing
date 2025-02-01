from sqlmodel import Session, SQLModel, select
from models.user import User

from db.engine import DatabaseManager, get_session

from fastapi import APIRouter, Request, HTTPException, Depends, Query

NO_USER_DESCRIPTION = "The ID of the user whose basket is requested"

router = APIRouter(
    prefix="/current-order",
    tags=["order"],
)

def check_user_and_order_existence(session: Session, user_id: int):
    user = User.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    order = user.get_current_order(session)

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

@router.put("/")
def get_current_order(session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    user = User.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user.get_current_order(session).load_relations(["basket.basket_items.variance.product"])

@router.put("/add-shipping-address")
async def add_shipping_address_to_current_order(request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    order = check_user_and_order_existence(session, user_id)

    data = await request.json()

    order.shipping_address = data.get("shipping_address")

    session.add(order)
    session.commit()

    session.refresh(order)

    return order.load_relations(["basket.basket_items.variance.product"])

@router.put("/add-billing-address")
async def add_billing_address_to_current_order(request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    order = check_user_and_order_existence(session, user_id)

    data = await request.json()

    if data.get("same_as_shipping_address", False):
        billing_address = order.shipping_address
    else:
        billing_address = data.get("billing_address")

    order.billing_address = billing_address

    session.add(order)
    session.commit()

    session.refresh(order)

    return order.load_relations(["basket.basket_items.variance.product"])

@router.put("/add-payment-method")
async def add_billing_address_to_current_order(request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    order = check_user_and_order_existence(session, user_id)

    data = await request.json()

    order.payment_method = data.get("payment_method")

    session.add(order)
    session.commit()

    session.refresh(order)

    return order.load_relations(["basket.basket_items.variance.product"])