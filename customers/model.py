from sqlalchemy import Boolean, Text, Column, Integer, String, DateTime, ForeignKey, Date
from database.database import Base
from sqlalchemy.orm import relationship


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=10), nullable=False)
    surname = Column(String(length=20), nullable=False)
    version = Column(Integer, default=0)
