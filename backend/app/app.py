import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user_router, product_router, variance_router, user_basket_router, order_user_router, order_router, inventory_router
from db.engine import DatabaseManager
#from init_db import init_db

from dotenv import load_dotenv

time.sleep(5)

load_dotenv()
DatabaseManager.initialize()

try:
    print("Attempting to initialize database with sample data...")
    from init_db import init_db
    init_db()
    print("Database initialization completed successfully")
except Exception as e:
    print(f"Warning: Database initialization failed: {str(e)}")

app = FastAPI()


#allow all origins for testing purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(variance_router.router)
app.include_router(user_basket_router.router)
app.include_router(order_user_router.router)
app.include_router(order_router.router)
app.include_router(inventory_router.router)

@app.get("/")
def read_root():
    return "Welcome to our shop!"