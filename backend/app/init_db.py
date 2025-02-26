from sqlmodel import Session
from db.engine import engine
from models.product import Product
from models.variance import Variance

def init_db():
    """Initialize the database with sample products and variances."""
    with Session(engine) as session:
        # Check if the product already exists
        existing_product = session.query(Product).filter(Product.id == 1).first()
        if existing_product:
            print("Product with ID 1 already exists. Skipping initialization.")
            return

        # Create the Athene product
        athene_bed = Product(
            id=1,
            name="Athene Furniture",
            furniture_type="bed",
            product_type="children bed",
            height=90.0,
            width=90.0,
            depth=190.0,
            base_price=790.00
        )

        session.add(athene_bed)
        session.commit()

        # Create a default variance for the product
        standard_variance = Variance(
            product_id=1,
            name="Standard",
            variance_type="default",
            price=790.00
        )

        session.add(standard_variance)
        session.commit()

        print("Database initialized with sample data.")

if __name__ == "__main__":
    init_db()
