from bills.schema import BillDisplay, BillMake, BillModel
from customers.model import Customers
from services.model import Appointments, Service
from orders.model import Order
from bikes.model import Bike
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from bills.model import Bill
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from bills.bill_template import html_template

def get_bills(db: Session):
    bills = db.query(Bill).all()
    return [BillDisplay(id=bill.id, customer_id=bill.customer_id, price=bill.price, document_title=bill.document_title) for bill in bills]

def post_bills(bill: BillMake, db: Session):
    customer = db.query(Customers).filter(Customers.id == bill.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="There is no customer")
    
    products = []
    total_price = 0
    for appointment_id in bill.appointments_ids:
        appointment = db.query(Appointments).filter(Appointments.id == appointment_id).first()
        if not appointment:
            continue
        if appointment.customer_id != bill.customer_id:
            continue
        for service in appointment.services:
            service = db.query(Service).filter(Service.id == service).first()
            total_price+=int(service.price)
            products.append({"lp": len(products), "name": service.name, "ilość": 1, "cena": service.price})
        try:
            appointment.posted = True
            db.commit()
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to mark appointment as posted. Error: {e}")
    for order_id in bill.orders_ids:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            continue
        if order.customer_id != bill.customer_id:
            continue
        
        bike = db.query(Bike).filter(Bike.id == order.bike_id).first()
        total_price+=int(bike.price)
        products.append({"lp": len(products), "name": bike.brand, "ilość": 1, "cena": bike.price})
        try:
            order.posted = True
            db.commit()
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to mark appointment as posted.")
    
    table_rows=make_billtable(products)
    
    formatted_html = html_template.format(
        table_rows=table_rows,
        total_price=total_price,
        buyer_nip=bill.nip,
        buyer=customer.name+" "+customer.surname
    )  

    try:
        max_id = db.query(func.max(Bill.id)).scalar()
        new_id = max_id + 1 if max_id else 1 
        db_appointment = Bill(id=new_id, customer_id=bill.customer_id, price=total_price,appointment_ids=bill.appointments_ids, orders_ids=bill.orders_ids, document_title=customer.name+" "+customer.surname, bill_content=formatted_html)
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return formatted_html

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create bill Error: {}".format(str(e))) 

def get_bill(id, db):
    try:
        bill = db.query(Bill).filter(Bill.id == id).first()
        if not bill:
            raise HTTPException(status_code=404, detail="Bill not found")
        
        return bill.bill_content
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get bill. Error: {}".format(str(e))) 


def delete_bill(id: int, db: Session):
    try:
        bill = db.query(Bill).filter(Bill.id == id).first()
        for appointment_id in bill.appointment_ids:
            appointment = db.query(Appointments).filter(Appointments.id == appointment_id).first()
            appointment.posted=False
        for order_id in bill.orders_ids:
            order = db.query(Order).filter(Order.id == order_id).first()
            order.posted=False
        db.delete(bill)
        db.commit
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete bill. Error: {}".format(str(e))) 

def make_billtable(products):
    table_rows = ""
    for product in products:
        table_rows += f"""
        <tr>
            <td>{product["lp"]}</td>
            <td>{product["name"]}</td>
            <td>{product["ilość"]}</td>
            <td>{product["cena"]}</td>
        </tr>
        """
    return table_rows

