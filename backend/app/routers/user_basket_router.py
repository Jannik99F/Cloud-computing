from sqlmodel import Session, SQLModel, select
from models.basket import Basket
from models.user import User
from models.variance import Variance
from models.basket_item import BasketItem

from db.engine import DatabaseManager, get_session

from fastapi import APIRouter, Request, HTTPException, Depends, Query

def check_user_exists(user_id: int):
    statement = select(User).where(User.id == user_id)
    user = get_session().exec(statement).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

router = APIRouter(
    prefix="/current-basket",
    tags=["current-basket"],
)

def get_current_basket_model(user_id: int, session: Session):
    check_user_exists(user_id)
    # TODO: Here, a real query is needed fetching the current basket for user.
    # The plan is to determine which is the current basket based on a basket
    # being already included in an order. The one basket, which is not included
    # in an order currently is the current one.
    statement = (
        select(Basket)
        .where(Basket.user_id == user_id)
        .order_by(Basket.id.desc())
        .limit(1)
    )
    basket = session.exec(statement).first()

    if basket is None:
        basket = new_basket = Basket(user_id=user_id)
        session.add(new_basket)
        session.commit()
        session.refresh(new_basket)

    return basket

def get_basket_item(basket_item_id: int, session: Session):
    statement = select(BasketItem).where(BasketItem.id == basket_item_id)
    return session.exec(statement).first()

@router.put("/")
def get_current_basket(session: Session = Depends(get_session), user_id: int = Query(..., description="The ID of the user whose basket is requested")):
    return get_current_basket_model(user_id, session).load_relations(relations_to_load=['basket_items'])

@router.put("/add-item")
async def add_item_to_current_basket(request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description="The ID of the user whose basket is requested")):
    basket = get_current_basket_model(user_id, session)

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

    return basket.load_relations(relations_to_load=['basket_items'])

@router.delete("/remove-item/{basket_item_id}")
async def add_item_to_current_basket(basket_item_id: int, session: Session = Depends(get_session)):
    statement = select(BasketItem).where(BasketItem.id == basket_item_id)
    basket_item = session.exec(statement).first()

    if basket_item is None:
        raise HTTPException(status_code=404, detail="BasketItem not found.")

    session.delete(basket_item)
    session.commit()

    return {"message": "BasketItem deleted successfully."}

@router.put("/item/{basket_item_id}/add")
async def add_item_to_current_basket(basket_item_id: int, request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description="The ID of the user whose basket is requested")):
    basket_item = get_basket_item(basket_item_id, session)

    if basket_item is None:
        raise HTTPException(status_code=404, detail="BasketItem not found.")

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

    return get_current_basket_model(user_id, session).load_relations(relations_to_load=['basket_items'])

@router.put("/item/{basket_item_id}/remove")
async def remove_item_from_current_basket(basket_item_id: int, request: Request, session: Session = Depends(get_session), user_id: int = Query(..., description="The ID of the user whose basket is requested")):
    basket_item = get_basket_item(basket_item_id, session)

    if basket_item is None:
        raise HTTPException(status_code=404, detail="BasketItem not found.")

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

    return get_current_basket_model(user_id, session).load_relations(relations_to_load=['basket_items'])
