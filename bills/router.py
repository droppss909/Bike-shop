from fastapi import APIRouter

from fastapi import Depends, HTTPException
from fastapi.responses import HTMLResponse
from database.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from bills.schema import BillModel, BillMake
from bills.model import Bill
from bills.service import get_bills, post_bills, get_bill, delete_bill

router = APIRouter(prefix="/bills", tags=["bills"])


@router.get("/")
def get_list_bills(db: Session = Depends(get_db)):
    return get_bills(db)

@router.post("/")
def post_bills_router(bill: BillMake, db: Session = Depends(get_db)):
    return post_bills(bill,db)

@router.get("/{id}")
def get_bill_router(id: int, db: Session = Depends(get_db)):
    bill_content = get_bill(id, db)
    return HTMLResponse(content=bill_content, status_code=200)

@router.delete("/{id}")
def delete_bill_router(id: int, db: Session = Depends(get_db)):
    return delete_bill(id, db)