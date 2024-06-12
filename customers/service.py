from customers.schema import CustomerModel, CustomerCreate
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from customers.model import Customers
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload


def get_customers(db: Session):
    try:
        customers = db.query(Customers).all()
        valid_customers = [
            CustomerModel(
                id=customer.id,
                name=customer.name,
                surname=customer.surname
            )
            for customer in customers if not(customer.name == " ") and not(customer.surname == " ")
        ]
        return valid_customers
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get customers. Error: {}".format(str(e)))
def get_customer(id: int, db: Session):
    try:
        customer = db.query(Customers).filter(Customers.id == id).first()
        return CustomerModel(id=customer.id, name=customer.name, surname=customer.surname)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get customer. Error: {}".format(str(e)))

def get_amount_of_customers(amount: int, db: Session):
    customers = db.query(Customers).limit(amount).all()
    return [CustomerModel(id=customer.id, name=customer.name, surname=customer.surname) for customer in customers]
 
def add_customer(db):
    try:
        max_id = db.query(func.max(Customers.id)).scalar()
        new_id = max_id + 1 if max_id else 1 
        db_customer = Customers(id=new_id, name=" ", surname=" ")
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
    user_provided_version = customer_data.get('version')
    
    if user_provided_version is None:
        raise HTTPException(status_code=400, detail="Version not provided")

    customer = db.query(Customers).filter(Customers.id == id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    current_version = customer.version

    if user_provided_version != current_version:
        raise HTTPException(status_code=409, detail="Conflict: Customer has been updated by another transaction")

    try:
        for attr, value in customer_data.items():
            if hasattr(customer, attr) and attr != 'version':  
                setattr(customer, attr, value)

        customer.version += 1

        db.commit()
        db.refresh(customer)

        return customer
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update customer. Error: {str(e)}")