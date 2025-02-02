from sqlmodel import Field, SQLModel, Relationship, select, Session
from models.base_model import BaseModel
from models.basket import Basket
from typing import Optional
from datetime import datetime, timedelta
from tasks.celery_app import celery_app
from db.engine import get_session
import random
from enums.enums import OrderStatus

class Order(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    shipping_address: Optional["str"]
    billing_address: Optional["str"]
    payment_method: Optional["str"]
    payment_secret: Optional["str"]
    payed: bool
    status: str
    basket_id: int = Field(default=None, foreign_key="basket.id")
    basket: "Basket" = Relationship(back_populates="order")

    def current_payment_secret(self, session: Session):
        if not self.payment_secret:
            self.status = OrderStatus.PAYMENT_STARTED.value

            session.add(self)
            session.commit()

            self.create_payment_secret(session)

        return self.payment_secret

    def create_payment_secret(self, session: Session):
        # I looked up on the internet how the payment process would work.
        # Assuming we are for now supporting PayPal only, the backend
        # would create some secret string with the PayPal API containing
        # how much has to be paid to which account. This secret is here
        # passed back to the frontend. With this secret in the frontend
        # the PayPal window can be opened showing the user what he is paying
        # for. To the secret via a standard format the order details can
        # be added to, so the user can lookup in the PayPal window what
        # he/she is paying for.

        # So here the PayPal API would be called and the secret would be created.
        payment_secret = "Some secret containing payment method, order details and who to pay to."

        session.add(self)
        session.commit()

        return payment_secret

    def is_payed(self, session: Session):
        # Right here, after the user calls the API to tell the payment
        # process is done, the order itself checks whether this is true
        # based on the secret. If it is the function returns true to finish
        # the order.
        payed = random.choice([True, False])

        if not payed:
            return False

        self.payed = True
        self.status = OrderStatus.PAYMENT_COMPLETED.value

        session.add(self)
        session.commit()

        return self.id

class TaskOrder:
    def __init__(self, order_id: int, expiration_minutes: int = 30):
        self.order_id = order_id
        self.expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)

    def start_expiration_timer(self):
        expire_order.apply_async(args=[self.order_id], eta=self.expiration_time)
        print(f"Order {self.order_id} will expire at {self.expiration_time}")

@celery_app.task
def expire_order(order_id: int):
    session = get_session()
    statement = select(Order).where(Order.id == order_id)
    order = session.exec(statement).first()

    statement = select(Basket).where(Basket.idf == order.basket_id)
    basket = session.exec(statement).first()
    if order and order.status != OrderStatus.PAYMENT_COMPLETED.value:
        session.delete(basket)
        session.commit()

        session.delete(order)
        session.commit()

    session.close()