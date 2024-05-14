from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class OrderModel(BaseModel):
    id: int
    customer_id: int
    bike_id: int
    posted: bool