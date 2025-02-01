from sqlmodel import Field, SQLModel, Relationship, select, Session
from typing import List, Optional
from models.base_model import BaseModel
from models.basket import Basket
from models.order import Order
from db.engine import get_session
from enums.enums import OrderStatus

from models.order import TaskOrder

class User(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    password: str
    address: str
    baskets: List["Basket"] = Relationship(back_populates="user", cascade_delete=True)

    @staticmethod
    def get_user(user_id: int) -> Optional["User"]:
        statement = select(User).where(User.id == user_id)

        return get_session().exec(statement).first()

    def get_current_basket(self, session: Session) -> Basket:
        # TODO: Here, a real query is needed fetching the current basket for user.
        # The plan is to determine which is the current basket based on a basket
        # being already included in an order. The one basket, which is not included
        # in an order currently is the current one.
        statement = (
            select(Basket)
            .where(Basket.user_id == self.id)
            .order_by(Basket.id.desc())
            .limit(1)
        )
        basket = session.exec(statement).first()

        if basket is None:
            basket = new_basket = Basket(user_id=self.id)
            session.add(new_basket)
            session.commit()
            session.refresh(new_basket)

        return basket

    def get_current_order(self, session: Session) -> Basket:
        statement = (
            select(Order)
            .where(Basket.user_id == self.id)
            .where(Order.status == OrderStatus.PENDING)
        )

        order = session.exec(statement).first()

        if order is None:
            order = new_order = Order(
                basket_id=self.get_current_basket(session).id,
                payed=False,
                status=OrderStatus.PENDING.value,
            )
            session.add(new_order)
            session.commit()
            session.refresh(new_order)

            task = TaskOrder(new_order.id)
            task.start_expiration_timer()

        return order