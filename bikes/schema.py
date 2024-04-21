from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class BikeModel(BaseModel):
    id: int
    brand: str
    model: str
    year: str
    price: str
    equipment: str
    color: str

class BikeCreate(BaseModel):
    brand: str
    model: str
    year: str
    price: str
    equipment: str
    color: str