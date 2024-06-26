from fastapi import APIRouter

from fastapi import Depends
from database.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from bikes.schema import BikeModel, BikeCreate
from bikes.service import get_bikes, get_amount_of_bikes, get_bike, add_bike, delete_bike, update_bike


router = APIRouter(prefix="/bikes", tags=["bikes"])

@router.get("/", response_model=list[BikeModel])
def get_list_bikes(db: Session = Depends(get_db)):
    return get_bikes(db)

@router.get("/{id}", response_model=BikeModel)
def get_bike_router(id: int, db: Session = Depends(get_db)):
    return get_bike(id,db)

@router.get("%{page}%{amount}", response_model=list[BikeModel])
def get_amount_of_bikes_router(page: int, amount: int, db: Session = Depends(get_db)):
    return get_amount_of_bikes(page, amount, db)

@router.post("/")
def add_bike_router(db: Session = Depends(get_db)):
    return add_bike(db)

@router.delete("/{id}")
def delete_bike_router(id: int, db: Session = Depends(get_db)):
    return delete_bike(id, db)

@router.put("/{id}")
def update_bike_router(id: int, customer_data: dict, db: Session = Depends(get_db)):
    return update_bike(id, customer_data, db)

    