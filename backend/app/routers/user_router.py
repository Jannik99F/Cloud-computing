from sqlmodel import Session, SQLModel, select
from models.user import User

from db.engine import DatabaseManager

from fastapi import APIRouter, Request, HTTPException

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
def get_all_users():
    with DatabaseManager.get_session() as session:
        statement = select(User)
        users = session.exec(statement).all()

    return {"users": users}

@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    with DatabaseManager.get_session() as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")

    return {"user": user}

@router.post("/")
async def create_user(request: Request):
    user_data = await request.json()

    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    email = user_data.get("email")
    password = user_data.get("password")
    address = user_data.get("address")

    with DatabaseManager.get_session() as session:
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            address=address
        )
        session.add(new_user)
        session.commit()

        session.refresh(new_user)

    return {"user": new_user.dict()}

@router.patch("/{user_id}")
async def update_user(user_id: int, request: Request):
    data = await request.json()

    with DatabaseManager.get_session() as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")

        for key, value in data.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)

        session.add(user)
        session.commit()

        session.refresh(user)

    return {"user": user.dict()}


@router.delete("/{user_id}")
def delete_user(user_id: int):
    with DatabaseManager.get_session() as session:
        user = session.get(User, user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")

        session.delete(user)
        session.commit()

    return {"message": "User deleted successfully."}
