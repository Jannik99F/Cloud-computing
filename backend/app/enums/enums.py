from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAYMENT_STARTED = "payment_started"
    PAYMENT_COMPLETED = "payment_completed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"

class PaymentMethod(str, Enum):
    PAY_PAL = "pay_pal"

class VarianceType(str, Enum):
    COLOR = "color"
    WOOD = "wood"

class FurnitureType(str, Enum):
    SEATING = "seating"
    STORAGE = "storage"
    SURFACE = "surface"
    SLEEP = "sleep"
    LIGHTING = "lighting"
    OUTDOOR = "outdoor"


class ProductType(str, Enum):
    # For Seating
    CHAIR = "chair"
    SOFA = "sofa"
    BENCH = "bench"

    # For Storage
    CABINET = "cabinet"
    BOOKSHELF = "bookshelf"
    WARDROBE = "wardrobe"
    SIDEBOARD = "sideboard"

    # For Surface
    TABLE = "table"
    DESK = "desk"
    CONSOLE_TABLE = "console_table"

    # For Sleep
    BED = "bed"
    BUNK_BED = "bunk_bed"
    FUTON = "futon"
    DAYBED = "daybed"

    # For Lighting
    LAMP = "lamp"
    CHANDELIER = "chandelier"
    SCONCE = "sconce"

    # For Outdoor
    PATIO_CHAIR = "patio_chair"
    HAMMOCK = "hammock"
    OUTDOOR_TABLE = "outdoor_table"

