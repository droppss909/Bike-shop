from fastapi import APIRouter

from fastapi import Depends
from database.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from orders.schema import OrderModel
from orders.model import Order
from orders.service import get_orders, get_order, post_orders, delete_order

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/")
def get_list_orders(db: Session = Depends(get_db)):
    return get_orders(db)

@router.get("/{id}")
def get_order_router(id: int, db: Session = Depends(get_db)):
    return get_order(id, db)

@router.post("/")
def post_orders_router(id_customer: int, ids_bikes: list[int], db: Session = Depends(get_db)):
   return post_orders(id_customer, ids_bikes, db)

@router.delete("/{id}")
def delete_order_router(id: int, db: Session = Depends(get_db)):
    return delete_order(id, db)