from sqlmodel import Session
from db.engine import engine, DatabaseManager
from models.product import Product
from models.variance import Variance
from models.inventory import Inventory
from models.user import User

def init_db():
    """Initialize the database with sample products, variances, inventory, and a test user."""
    # Ensure DB tables are created
    DatabaseManager.initialize()
    
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

        # Create variances for the product
        variances = [
            Variance(
                product_id=1,
                name="Standard White",
                variance_type="color",
                price=790.00
            ),
            Variance(
                product_id=1,
                name="Natural Wood",
                variance_type="color",
                price=850.00
            ),
            Variance(
                product_id=1,
                name="Navy Blue",
                variance_type="color",
                price=890.00
            )
        ]
        
        for variance in variances:
            session.add(variance)
        session.commit()
        
        # Add inventory for each variance
        for idx, variance in enumerate(variances):
            inventory = Inventory(
                variance_id=variance.id,
                amount=10 - idx  # Different stock levels for demo
            )
            session.add(inventory)
        session.commit()
        
        # Create a test user for demo
        test_user = User(
            first_name="Demo",
            last_name="User",
            email="demo@example.com",
            password="password123",  # In a real app, this would be hashed
            address="123 Demo Street, Demo City"
        )
        session.add(test_user)
        session.commit()

        print("Database initialized with sample data:")
        print("- 1 product with 3 color variances")
        print("- Inventory added for each variance")
        print("- Demo user created (email: demo@example.com)")

if __name__ == "__main__":
    init_db()
