from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class BillModel(BaseModel):
    customer_id: int
    price: str
    document_title: str
    bill_content: str


class BillDisplay(BaseModel):
    id: int
    customer_id: int
    price: str
    document_title: str  


class BillMake(BaseModel):
    customer_id: int
    nip: str
    appointments_ids: list[int]
    orders_ids: list[int]
