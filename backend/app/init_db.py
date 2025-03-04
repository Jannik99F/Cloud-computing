from sqlmodel import Session
from db.engine import DatabaseManager
from models.product import Product
from models.variance import Variance
from models.inventory import Inventory
from models.user import User
import random

def init_db():
    """Initialize the database with sample products, variances, inventory, and a test user."""
    # Ensure DB tables are created
    DatabaseManager.initialize()

    engine = DatabaseManager.get_engine()
    
    with Session(engine) as session:
        # Check if the product already exists
        existing_product = session.query(Product).filter(Product.id == 1).first()
        if existing_product:
            print("Product with ID 1 already exists. Skipping initialization.")
            return

        # Create all products
        products = [
            Product(
                id=1,
                name="Athene",
                furniture_type="Bed",
                product_type="Children Bed",
                height=90.0,
                width=90.0,
                depth=190.0,
                base_price=799.00
            ),
            Product(
                id=2,
                name="Aphrodite",
                furniture_type="Bed",
                product_type="Queen Size Bed",
                height=90.0,
                width=152.0,
                depth=203.0,
                base_price=1299.00
            ),
            Product(
                id=3,
                name="Napoleon",
                furniture_type="Bed",
                product_type="King Size Bed",
                height=90.0,
                width=152.0,
                depth=213.0,
                base_price=1599.00
            ),
            Product(
                id=4,
                name="Demeter",
                furniture_type="Table",
                product_type="Dining Table",
                height=75.0,
                width=305.0,
                depth=120.0,
                base_price=6999.00
            ),
            Product(
                id=5,
                name="Hades",
                furniture_type="Table",
                product_type="Bedside Table",
                height=45.0,
                width=60.0,
                depth=40.0,
                base_price=999.00
            ),
            Product(
                id=6,
                name="Hera",
                furniture_type="Table",
                product_type="Coffee Table",
                height=42.0,
                width=107.0,
                depth=53.0,
                base_price=3499.00
            ),
            Product(
                id=7,
                name="Nike",
                furniture_type="Cabinet",
                product_type="Wardrobe",
                height=212.0,
                width=227.0,
                depth=72.0,
                base_price=8999.00
            ),
            Product(
                id=8,
                name="Eileithyia",
                furniture_type="Cabinet",
                product_type="Kitchen Cupboard",
                height=82.0,
                width=97.0,
                depth=43.0,
                base_price=2499.00
            ),
            Product(
                id=9,
                name="Hermes",
                furniture_type="Chair",
                product_type="Dining Room Chair",
                height=93.0,
                width=45.0,
                depth=42.0,
                base_price=299.00
            ),
            Product(
                id=10,
                name="Dionysos",
                furniture_type="Chair",
                product_type="Armchair",
                height=102.0,
                width=57.0,
                depth=60.0,
                base_price=749.00
            ),
        ]
        
        # Add all products to database
        for product in products:
            session.add(product)
        session.commit()
        
        # Create color variances for each product
        all_variances = []
        
        # Common color options
        colors = [
            {"name": "Standard White", "price_factor": 1.0},
            {"name": "Natural Wood", "price_factor": 1.07},
            {"name": "Navy Blue", "price_factor": 1.12},
            {"name": "Dark Oak", "price_factor": 1.15},
            {"name": "Cherry Red", "price_factor": 1.18}
        ]
        
        # Create variances for each product
        for product in products:
            product_variances = []
            
            # Add 3-5 color variations for each product
            num_colors = random.randint(3, 5)
            selected_colors = random.sample(colors, num_colors)
            
            for color in selected_colors:
                variance_price = round(product.base_price * color["price_factor"], 2)
                variance = Variance(
                    product_id=product.id,
                    name=color["name"],
                    variance_type="color",
                    price=variance_price
                )
                session.add(variance)
                product_variances.append(variance)
            
            session.commit()
            all_variances.extend(product_variances)
            
            # Add inventory for each variance
            for idx, variance in enumerate(product_variances):
                stock = random.randint(5, 15)
                inventory = Inventory(
                    variance_id=variance.id,
                    amount=stock - (idx % 3)  # Varied stock levels
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
        print(f"- {len(products)} products added")
        print(f"- {len(all_variances)} color variances created")
        print("- Inventory added for each variance")
        print("- Demo user created (email: demo@example.com)")

if __name__ == "__main__":
    init_db()