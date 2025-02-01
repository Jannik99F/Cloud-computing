from sqlmodel import Field, SQLModel, Relationship, select
from models.base_model import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from tasks.celery_app import celery_app
from db.engine import get_session


class Order(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    shipping_address: Optional["str"]
    billing_address: Optional["str"]
    payment_method: Optional["str"]
    payed: bool
    status: str
    basket_id: int = Field(default=None, foreign_key="basket.id")
    basket: "Basket" = Relationship(back_populates="order")

class TaskOrder:
    def __init__(self, order_id: int, expiration_minutes: int = 30):
        self.order_id = order_id
        self.expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)

    def start_expiration_timer(self):
        expire_order.apply_async(args=[self.order_id], eta=self.expiration_time)
        print(f"⏳ Order {self.order_id} will expire at {self.expiration_time}")

@celery_app.task
def expire_order(order_id: int):
    session = get_session()
    statement = select(Order).where(Order.id == order_id)
    order = session.exec(statement).first()
    if order and order.status != "completed":
        session.delete(order)
        session.commit()