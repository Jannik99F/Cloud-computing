from sqlmodel import Field, SQLModel, Relationship, select, Session, or_
from typing import List
from models.base_model import BaseModel
from models.basket import Basket
from models.order import Order
from db.engine import get_session
from enums.enums import OrderStatus

from models.order import TaskOrder

from models.basket_item import BasketItem

class User(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    password: str
    address: str
    baskets: List["Basket"] = Relationship(back_populates="user", cascade_delete=True)

    @staticmethod
    def get_user(user_id: int):
        statement = select(User).where(User.id == user_id)

        return get_session().exec(statement).first()

    def get_current_basket(self, session: Session):
        statement = (
            select(Basket)
            .where(Basket.user_id == self.id)
            .order_by(Basket.id.desc())
            .limit(1)
        )
        basket = session.exec(statement).first()

        order = None
        if basket is not None:
            # The order in which the current basket might be included at the moment is
            # fetched, so it can be checked whether the current orders exists and the
            #  status is still pending. Only that allows the user to still edit it.
            order = session.exec(select(Order).where(Order.basket_id == basket.id)).first()

        if basket is None or (order is not None and order.status != OrderStatus.PENDING.value):
            basket = new_basket = Basket(user_id=self.id)
            session.add(new_basket)
            session.commit()
            session.refresh(new_basket)

        return basket

    def get_current_order(self, session: Session):
        statement = (select(Order)
                     .join(Basket)
                     .where(Basket.user_id == self.id)
                     .where(or_(Order.status == OrderStatus.PENDING.value,
                                Order.status == OrderStatus.PAYMENT_STARTED.value)))

        order = session.exec(statement).first()

        if order is None:
            basket = self.get_current_basket(session)

            if not basket:
                return None

            basket_items = session.exec(select(BasketItem).where(BasketItem.basket_id == basket.id)).first()

            if not basket_items:
                return None

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