from datetime import datetime, date
from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr, validator

class ServiceModel(BaseModel):
    name: str
    description: str
    price: str


class AppointmentModel(BaseModel):
    appointment_id: int
    customer_id: int
    date: str
    services: List[int]