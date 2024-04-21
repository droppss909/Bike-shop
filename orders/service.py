from orders.schema import OrderModel
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from orders.model import Order
from customers.model import Customers
from bikes.model import Bike
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload


def get_orders(db: Session):
    orders = db.query(Order).all()
    return [OrderModel(id=order.id, customer_id=order.customer_id, bike_id=order.bike_id, posted=order.posted) for order in orders]

def get_order(id: int, db: Session):
    try:
        order = db.query(Order).filter(Order.id == id).first()
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get order. Error: {}".format(str(e))) 

def post_orders(id_customer: int, ids_bikes: list[int], db: Session):
    not_exists_bikes=[]
    customer = db.query(Customers).filter(Customers.id == id_customer).first()
    if not customer:
        raise HTTPException(status_code=404, detail="There is no this customer")
    
    try:
        for id in ids_bikes:
            bike = db.query(Bike).filter(Bike.id == id).first()
            if bike:
                max_id = db.query(func.max(Order.id)).scalar()
                new_id = max_id + 1 if max_id else 1 
                db_order = Order(id=new_id, customer_id=id_customer, bike_id=id, posted=False)
                db.add(db_order)
                db.commit()
                db.refresh(db_order)
            else:
                not_exists_bikes.append(id)
        if not not_exists_bikes:
            return {"acknowledge"}
        else:
            return {"post orders except": not_exists_bikes}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create order. Error: {}".format(str(e)))

def delete_order(id, db):
    order = db.query(Order).filter(Order.id == id).first()

    if not order:
        raise HTTPException(status_code=404, detail="order not found")

    try:
        db.delete(order)
        db.commit()
        return {"message": "order deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete order. Error: {}".format(str(e))) 
 