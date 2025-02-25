import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user_router, product_router, variance_router, user_basket_router, order_user_router, order_router, inventory_router
from db.engine import DatabaseManager

from dotenv import load_dotenv

time.sleep(5)

load_dotenv()
DatabaseManager.initialize()

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