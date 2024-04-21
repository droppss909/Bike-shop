from sqlalchemy import Boolean, Text, Column, Integer, String, DateTime, ForeignKey, Date
from database.database import Base
from sqlalchemy.orm import relationship


class Bike(Base):
    __tablename__ = "bikes"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(length=10), nullable=False)
    model = Column(String(length=20), nullable=False)
    year = Column(String(length=5), nullable=False)
    price = Column(String(length=5), nullable=False)
    equipment = Column(String(length=20), nullable=False)
    color = Column(String(length=10), nullable=True)


