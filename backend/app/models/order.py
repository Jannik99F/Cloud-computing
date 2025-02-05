from sqlmodel import Field, SQLModel, Relationship, select, Session
from models.base_model import BaseModel
from models.basket import Basket
from models.inventory import Inventory
from typing import Optional
from datetime import datetime, timedelta
from tasks.celery_app import celery_app
from db.engine import get_session

from enums.enums import OrderStatus

class Order(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    shipping_address: Optional["str"]
    billing_address: Optional["str"]
    payment_method: Optional["str"]
    payment_secret: Optional["str"]
    payed: bool
    items_reserved: bool
    status: str
    basket_id: int = Field(default=None, foreign_key="basket.id", ondelete="CASCADE")
    basket: "Basket" = Relationship(back_populates="order")

    def current_payment_secret(self, session: Session):
        if not self.payment_secret:
            self.status = OrderStatus.PAYMENT_STARTED.value

            session.add(self)
            session.commit()

            self.create_payment_secret(session)

        return self.payment_secret

    def set_basket_items_price(self, session: Session):
        # Right here, the basket_items prices will be set to the current prices.
        # If the prices for a product or its variance will be edited this won't
        # affect the order and the prices at the time when it was bought will be
        # kept to be able to do refunds if necessary.

        for basket_item in self.basket.basket_items:
            basket_item.base_price = basket_item.variance.product.base_price
            basket_item.variance_price = basket_item.variance.price

            session.add(basket_item)
            session.commit()

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

        self.payment_secret = payment_secret

        session.add(self)
        session.commit()

        return payment_secret

    def is_payed(self, session: Session):
        # Right here, after the user calls the API to tell the payment
        # process is done, the order itself checks whether this is true
        # based on the secret. If it is the function returns true to finish
        # the order.

        # Here the paypal API would be called based on the secret to check
        # whether the user payed.
        payed = True

        if not payed:
            return False

        self.payed = True
        self.status = OrderStatus.PAYMENT_COMPLETED.value

        session.add(self)
        session.commit()

        return self.id

    def pay_money_back(self):
        print("The money is payed back to the user.")

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

    if order and order.status != OrderStatus.PAYMENT_COMPLETED.value:
        # When the user payed in the popout window of paypal but didn't
        # afterwards no our website again confirm the purchase, the money
        # will be payed back to the user and the order is deleted/cancelled.
        if order.is_payed(session):
            order.pay_money_back()

        # The reserved items will be put back into the stock if the
        # payment process wasn't completed and the order will be
        # deleted because it is unfinished.
        if order.items_reserved:
            for basket_item in order.basket.basket_items:
                statement = select(Inventory).where(Inventory.variance_id == basket_item.variance_id)
                variance_for_inventory = session.execute(statement).scalar_one_or_none()

                try:
                    variance_for_inventory.amount += basket_item.amount
                except Exception:
                    print("It looks like someone removed the inventory item. The amount included in the order can't be added again.")

                session.add(variance_for_inventory)

        basket = order.basket

        session.delete(basket)

        session.commit()

    session.close()