from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class CustomerModel(BaseModel):
    id: int
    name: str
    surname: str

class CustomerCreate(BaseModel):
    name: str
    surname: str
