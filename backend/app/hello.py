from fastapi import FastAPI
from sqlmodel import Session, Field, SQLModel, create_engine, select

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = database_url = os.getenv("DB_URL_LOCAL") if os.getenv("DEBUG") == "true" else os.getenv("DB_URL_PROD")
engine = create_engine(DATABASE_URL)

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    password: str
    address: str

app = FastAPI()

@app.get("/")
def read_root():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        statement = select(User).where(User.first_name == "Tim")
        user = session.exec(statement).first()

        if(not user):
            user = User(id=1, first_name="Tim", last_name="Finmans", email="tim@finmans.de", password="tim123", address="123 Main Street")
            session.add(user)
            session.commit()

    return {"user": user}