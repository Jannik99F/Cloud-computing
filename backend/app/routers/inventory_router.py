from sqlmodel import Session, select
from models.inventory import Inventory
from models.variance import Variance

from db.engine import DatabaseManager, get_session

from fastapi import APIRouter, Request, HTTPException, Depends, Query

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
)

def check_variance_and_inventory_existence(variance_id: int, session: Session):
    statement = select(Variance).where(Variance.id == variance_id)
    variance = session.exec(statement).first()

    if variance is None:
        raise HTTPException(status_code=404, detail="Variance not found.")

    statement = select(Inventory).where(Inventory.variance_id == variance.id)
    variance_for_inventory = session.exec(statement).first()

    if variance_for_inventory is None:
        raise HTTPException(status_code=404, detail="Variance not in the inventory yet.")

    return variance_for_inventory

@router.get("/")
def get_inventory_items(session: Session = Depends(get_session)):
    statement = select(Inventory)
    inventory_items = session.exec(statement).all()

    session.close()

    return inventory_items

@router.get("/{variance_id}")
def get_inventory_item_by_id(variance_id: int, session: Session = Depends(get_session)):
    statement = select(Inventory).where(Inventory.variance_id == variance_id)
    inventory_item = session.exec(statement).all()

    session.close()

    return inventory_item

@router.post("/")
async def add_inventory_item(request: Request, session: Session = Depends(get_session)):
    variance_data = await request.json()

    variance_id = variance_data.get("variance_id")
    amount = variance_data.get("amount")

    statement = select(Variance).where(Variance.id == variance_id)
    variance = session.exec(statement).first()

    if variance is None:
        raise HTTPException(status_code=404, detail="Variance not found.")

    statement = select(Inventory).where(Inventory.variance_id == variance.id)
    variance_for_inventory = session.exec(statement).first()

    if variance_for_inventory:
        variance_for_inventory.amount += amount
    else:
        variance_for_inventory = Inventory(
            variance_id=variance_id,
            amount=amount,
        )

    session.add(variance_for_inventory)
    session.commit()

    session.refresh(variance_for_inventory)

    session.close()

    return variance_for_inventory

@router.delete("/{variance_id}")
async def delete_inventory_item(variance_id: int, session: Session = Depends(get_session)):
    variance_for_inventory = check_variance_and_inventory_existence(variance_id, session)

    session.delete(variance_for_inventory)
    session.commit()

    session.close()

    return {"message": "Inventory variance deleted successfully."}

@router.put("/item/{variance_id}/add")
async def higher_inventory_item_amount(variance_id: int, request: Request, session: Session = Depends(get_session)):
    variance_for_inventory = check_variance_and_inventory_existence(variance_id, session)

    try:
        variance_amount_data = await request.json()
    except Exception as e:
        variance_amount_data = {}

    additional_amount = variance_amount_data.get("additional_amount", None)

    if additional_amount:
        if additional_amount < 0:
            raise HTTPException(status_code=400, detail="Additional amount must be greater than 0.")

        variance_for_inventory.amount += additional_amount
    else:
        variance_for_inventory.amount += 1

    session.add(variance_for_inventory)
    session.commit()

    session.refresh(variance_for_inventory)

    session.close()

    return variance_for_inventory

@router.put("/item/{variance_id}/remove")
async def lower_inventory_item_amount(variance_id: int, request: Request, session: Session = Depends(get_session)):
    variance_for_inventory = check_variance_and_inventory_existence(variance_id, session)

    try:
        variance_amount_data = await request.json()
    except Exception as e:
        variance_amount_data = {}

    removal_amount = variance_amount_data.get("removal_amount", None)

    if removal_amount:
        if removal_amount < 0:
            raise HTTPException(status_code=400, detail="Removal amount must be greater than 0.")

        variance_for_inventory.amount -= removal_amount
    else:
        variance_for_inventory.amount -= 1

    if variance_for_inventory.amount < 0:
        raise HTTPException(status_code=400, detail="Amount cannot go below 0.")

    session.add(variance_for_inventory)
    session.commit()

    session.refresh(variance_for_inventory)

    session.close()

    return variance_for_inventory