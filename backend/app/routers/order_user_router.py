from sqlmodel import Session, SQLModel, select
from models.user import User

from db.engine import DatabaseManager, get_session

from fastapi import APIRouter, Request, HTTPException, Depends, Query

from enums.enums import OrderStatus

from models.inventory import Inventory

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
        raise HTTPException(status_code=400, detail="No order found.")

    return order

@router.put("/")
def get_current_order(session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    user = User.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    order = check_user_and_order_existence(session, user_id).load_relations(["basket.basket_items.variance.product"])

    session.close()

    return order

@router.put("/add-shipping-address")
async def add_shipping_address(request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    order = check_user_and_order_existence(session, user_id)

    if order.status != OrderStatus.PENDING.value:
        raise HTTPException(status_code=400, detail="Order not pending.")

    data = await request.json()

    order.shipping_address = data.get("shipping_address")

    session.add(order)
    session.commit()

    session.refresh(order)

    order = order.load_relations(["basket.basket_items.variance.product"])

    session.close()

    return order

@router.put("/add-billing-address")
async def add_billing_address(request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    order = check_user_and_order_existence(session, user_id)

    if order.status != OrderStatus.PENDING.value:
        raise HTTPException(status_code=400, detail="Order not pending.")

    data = await request.json()

    if data.get("same_as_shipping_address", False):
        billing_address = order.shipping_address
    else:
        billing_address = data.get("billing_address")

    order.billing_address = billing_address

    session.add(order)
    session.commit()

    session.refresh(order)

    order = order.load_relations(["basket.basket_items.variance.product"])

    session.close()

    return order

@router.put("/add-payment-method")
async def add_payment_method(request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    order = check_user_and_order_existence(session, user_id)

    if order.status != OrderStatus.PENDING.value:
        raise HTTPException(status_code=400, detail="Order not pending.")

    data = await request.json()

    order.payment_method = data.get("payment_method")

    session.add(order)
    session.commit()

    session.refresh(order)

    order.load_relations(["basket.basket_items.variance.product"])

    session.close()

    return order

@router.put("/pay")
async def pay(session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    order = check_user_and_order_existence(session, user_id)

    if order.shipping_address is None or order.billing_address is None or order.payment_method is None:
        raise HTTPException(status_code=400, detail="There aren't yet all order information provided.")

    if order.status != OrderStatus.PENDING.value and order.status != OrderStatus.PAYMENT_STARTED.value:
        raise HTTPException(status_code=400, detail="Order not in the right state.")

    if order.status == OrderStatus.PAYMENT_STARTED.value:
        return order.current_payment_secret(session)

    order.set_basket_items_price(session)

    # Try to reserve all the items. If for some are not enough in stock,
    # an HTTPException is send back and the user sees of which item
    # he/she wants to order "to many"
    for basket_item in order.basket.basket_items:
        statement = select(Inventory).where(Inventory.variance_id == basket_item.variance_id)
        variance_for_inventory = session.execute(statement).scalar_one_or_none()

        if variance_for_inventory is None:
            raise HTTPException(status_code=404, detail="This item is not in stock.")

        if variance_for_inventory.amount < basket_item.amount:
            raise HTTPException(status_code=400, detail="The item " + str(basket_item.variance.product.name) + " with the variance " + str(basket_item.variance.name) + " is not available in that amount. Just " + str(variance_for_inventory.amount) + " of that item are available.")
        else:
            variance_for_inventory.amount -= basket_item.amount

        session.add(variance_for_inventory)

    order.items_reserved = True
    session.add(order)

    payment_secret = order.current_payment_secret(session)

    session.commit()
    session.close()

    return payment_secret

@router.post("/checkout")
async def checkout(session: Session = Depends(get_session), user_id: int = Query(..., description=NO_USER_DESCRIPTION)):
    order = check_user_and_order_existence(session, user_id)

    if order.status != OrderStatus.PAYMENT_STARTED.value:
        raise HTTPException(status_code=400, detail="Payment not started.")

    if order.payed:
        raise HTTPException(status_code=400, detail="Payment already confirmed.")

    if not order.is_payed(session):
        raise HTTPException(status_code=404, detail="Couldn't confirm the payment.")

    order = order.load_relations(["basket.basket_items.variance.product"])

    session.close()

    # TODO: A confirmation mail needs to be send.

    return order