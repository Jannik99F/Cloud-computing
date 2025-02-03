from sqlmodel import Session, SQLModel, select
from models.user import User
from models.variance import Variance
from models.basket_item import BasketItem
from models.basket import Basket
from models.order import Order

from db.engine import DatabaseManager, get_session

from fastapi import APIRouter, Request, HTTPException, Depends, Query

router = APIRouter(
    prefix="/current-basket",
    tags=["current-basket"]
)

def get_basket_item(user: User, basket_item_id: int, session: Session):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    basket = user.get_current_basket(session)

    statement = select(BasketItem).where(BasketItem.id == basket_item_id).where(BasketItem.basket_id == basket.id)
    basket_item = session.exec(statement).first()

    if basket_item is None:
        raise HTTPException(status_code=404, detail="BasketItem not found.")

    return basket_item

# The decision was made to only allow orders having basket which has at least
# one BasketItem. When a BasketItem is removed and the Basket gets empty,
# the order has to be removed as well.
def check_existing_order_must_be_deleted(basket: Basket ,session: Session):
    statement = select(BasketItem).where(BasketItem.basket_id == basket.id)
    basket_item = session.exec(statement).first()

    statement = select(Order).where(Order.basket_id == basket.id)
    order = session.exec(statement).first()

    if basket_item is None and order is not None:
        session.delete(order)
        session.commit()

@router.put("/")
def get_current_basket(session: Session = Depends(get_session), user_id: int = Query(..., description="The ID of the user whose basket is requested")):
    user = User.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    basket = user.get_current_basket(session).load_relations(relations_to_load=['basket_items'])

    session.close()

    return basket

@router.post("/add-item")
async def add_item_to_current_basket(request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description="The ID of the user whose basket is requested")):
    user = User.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    basket = user.get_current_basket(session)

    item_data = await request.json()

    variance_id = item_data.get("variance_id")
    amount = item_data.get("amount")

    statement = select(Variance).where(Variance.id == variance_id)
    variance = session.exec(statement).first()

    if variance is None:
        raise HTTPException(status_code=404, detail="Variance not found.")

    statement = (select(BasketItem)
                 .where(BasketItem.variance_id == variance.id)
                 .where(BasketItem.basket_id == basket.id))

    if session.exec(statement).first() is not None:
        raise HTTPException(status_code=400, detail="A BasketItem with for this variance already exists.")

    basket_item = BasketItem(
        basket_id=basket.id,
        variance_id=variance_id,
        amount=amount,
        base_price=None,
        variance_price=None
    )
    session.add(basket_item)
    session.commit()

    session.refresh(basket_item)

    basket = basket.load_relations(relations_to_load=['basket_items'])

    session.close()

    return basket

@router.delete("/remove-item/{basket_item_id}")
async def add_item_to_current_basket(basket_item_id: int, session: Session = Depends(get_session), user_id: int = Query(..., description="The ID of the user whose basket is requested")):
    basket_item = get_basket_item(User.get_user(user_id), basket_item_id, session)

    basket = basket_item.basket

    session.delete(basket_item)
    session.commit()

    check_existing_order_must_be_deleted(basket, session)

    session.close()

    return {"message": "BasketItem deleted successfully."}

@router.put("/item/{basket_item_id}/add")
async def add_item_to_current_basket(basket_item_id: int, request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description="The ID of the user whose basket is requested")):
    basket_item = get_basket_item(User.get_user(user_id), basket_item_id, session)

    try:
        item_data = await request.json()
    except Exception as e:
        item_data = {}

    additional_amount = item_data.get("additional_amount", None)

    if additional_amount:
        if additional_amount < 0:
            raise HTTPException(status_code=400, detail="Additional amount must be greater than 0.")

        basket_item.amount += additional_amount
    else:
        basket_item.amount += 1

    session.add(basket_item)
    session.commit()

    user = User.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    basket = user.get_current_basket(session).load_relations(relations_to_load=['basket_items'])

    session.close()

    return basket

@router.put("/item/{basket_item_id}/remove")
async def remove_item_from_current_basket(basket_item_id: int, request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description="The ID of the user whose basket is requested")):
    basket_item = get_basket_item(User.get_user(user_id), basket_item_id, session)

    try:
        item_data = await request.json()
    except Exception as e:
        item_data = {}

    removal_amount = item_data.get("removal_amount", None)

    if removal_amount:
        if removal_amount < 0:
            raise HTTPException(status_code=400, detail="Additional amount must be greater than 0.")
        basket_item.amount -= removal_amount
    else:
        basket_item.amount -= 1

    if basket_item.amount < 1:
        raise HTTPException(status_code=400, detail="Amount cannot go below 1.")

    session.add(basket_item)
    session.commit()

    user = User.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    basket = user.get_current_basket(session).load_relations(relations_to_load=['basket_items'])

    session.close()

    return basket
