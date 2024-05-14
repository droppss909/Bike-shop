from fastapi import APIRouter

from fastapi import Depends
from database.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from customers.schema import CustomerModel, CustomerCreate
from customers.model import Customers
from customers.service import get_customers, get_customer, add_customer, delete_customer, update_customer


router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/", response_model=list[CustomerModel])
def get_list_customers(db: Session = Depends(get_db)):
    return get_customers(db)

@router.get("/{id}", response_model=CustomerModel)
def get_customer_router(id: int, db: Session = Depends(get_db)):
    return get_customer(id,db)

@router.post("/")
def add_customer_router(db: Session = Depends(get_db)):
    return add_customer(db)

@router.delete("/{id}")
def delete_customer_router(id: int, db: Session = Depends(get_db)):
    return delete_customer(id, db)

@router.put("/{id}")
def update_customer_router(id: int, customer_data: dict, db: Session = Depends(get_db)):
    return update_customer(id, customer_data, db)