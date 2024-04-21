from sqlalchemy import Boolean, Text, Column, Integer, String, DateTime, ForeignKey, Date
from database.database import Base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=20), nullable=False)
    description = Column(String(length=200), nullable=True)
    price = Column(String(length=20), nullable=False)


class Appointments(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    date = Column(String(length=20), nullable=False)
    services = Column(ARRAY(Integer))
    posted = Column(Boolean, nullable=False)