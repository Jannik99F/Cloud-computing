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
        raise HTTPException(status_code=404, detail="User not found.")

    order = user.get_current_order(session)

    if order is None:
        raise HTTPException(status_code=400, detail="No items in the basket yet for which an order could be placed.")

    # TODO: here needs to be checked that only pending orders will be edited.

    return order

@router.put("/")
def get_current_order(session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    user = User.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return check_user_and_order_existence(session, user_id).load_relations(["basket.basket_items.variance.product"])

@router.put("/add-shipping-address")
async def add_shipping_address(request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    order = check_user_and_order_existence(session, user_id)

    data = await request.json()

    order.shipping_address = data.get("shipping_address")

    session.add(order)
    session.commit()

    session.refresh(order)

    return order.load_relations(["basket.basket_items.variance.product"])

@router.put("/add-billing-address")
async def add_billing_address(request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
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
async def add_payment_method(request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    order = check_user_and_order_existence(session, user_id)

    data = await request.json()

    order.payment_method = data.get("payment_method")

    session.add(order)
    session.commit()

    session.refresh(order)

    return order.load_relations(["basket.basket_items.variance.product"])

@router.put("/pay")
async def pay(session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    order = check_user_and_order_existence(session, user_id)

    if order.shipping_address is None or order.billing_address is None or order.payment_method is None:
        raise HTTPException(status_code=400, detail="There aren't yet all order information provided.")

    return order.current_payment_secret(session)

@router.post("/checkout")
async def checkout(session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    order = check_user_and_order_existence(session, user_id)

    if not order.payment_secret:
        raise HTTPException(status_code=400, detail="Payment process not initialized yet.")

    if order.payed:
        raise HTTPException(status_code=400, detail="Payment already confirmed.")

    if not order.is_payed(session):
        raise HTTPException(status_code=404, detail="Couldn't confirm the payment.")

    # TODO: Right here to order would really be placed and the shipping process started with an confirmation email.

    return order.load_relations(["basket.basket_items.variance.product"])