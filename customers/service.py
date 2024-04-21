from customers.schema import CustomerModel, CustomerCreate
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from customers.model import Customers
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload


def get_customers(db):
    customers = db.query(Customers).all()
    return [CustomerModel(id=customer.id, name=customer.name, surname=customer.surname) for customer in customers]

def get_customer(id: int, db: Session):
    try:
        customer = db.query(Customers).filter(Customers.id == id).first()
        return CustomerModel(id=customer.id, name=customer.name, surname=customer.surname)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get customer. Error: {}".format(str(e))) 

def add_customer(customer, db):
    try:
        max_id = db.query(func.max(Customers.id)).scalar()
        new_id = max_id + 1 if max_id else 1 
        db_customer = Customers(id=new_id, **customer.dict())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return {"acknowledge"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create customer. Error: {}".format(str(e))) 
    
def delete_customer(id: int, db: Session):
    customer = db.query(Customers).filter(Customers.id == id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    try:
        db.delete(customer)
        db.commit()
        return {"message": "Customer deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete customer. Error: {}".format(str(e))) 

def update_customer(id: int, customer_data: dict, db: Session):
    customer = db.query(Customers).filter(Customers.id == id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    try:
        for attr, value in customer_data.items():
            if hasattr(customer, attr):
                setattr(customer, attr, value)
        
        db.commit()
        db.refresh(customer)
        
        return customer

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update customer. Error: {str(e)}")