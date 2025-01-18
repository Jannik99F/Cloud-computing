import time

from fastapi import FastAPI
from routers import user_router
from db.engine import DatabaseManager

from dotenv import load_dotenv

time.sleep(5)

load_dotenv()
DatabaseManager.initialize()

app = FastAPI()

app.include_router(user_router.router)

@app.get("/")
def read_root():
    return "123"