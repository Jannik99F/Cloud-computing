from sqlmodel import Session, SQLModel, select
from models.basket import Basket
from models.user import User
from models.basket_item import BasketItem

from db.engine import DatabaseManager, get_session

from fastapi import APIRouter, Request, HTTPException, Depends

def check_user_exists(user_id: int):
    statement = select(User).where(User.id == user_id)
    user = get_session().exec(statement).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

router = APIRouter(
    prefix="/users/{user_id}",
    tags=["basket"],
    dependencies=[Depends(check_user_exists)],
)

@router.put("/current-basket")
def get_basket_by_id(user_id: int, session: Session = Depends(get_session)):
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

"""
@router.post("/")
async def create_user(request: Request, session: Session = Depends(get_session)):
    user_data = await request.json()

    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    email = user_data.get("email")
    password = user_data.get("password")
    address = user_data.get("address")

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        address=address
    )
    session.add(new_user)
    session.commit()

    session.refresh(new_user)

    return new_user
"""