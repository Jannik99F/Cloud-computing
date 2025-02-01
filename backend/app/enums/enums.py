from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAYMENT_STARTED = "payment_started"
    PAYMENT_COMPLETED = "payment_completed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"