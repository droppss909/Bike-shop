from sqlalchemy import Boolean, Text, Column, Integer, String, DateTime, ForeignKey, Date
from database.database import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    bike_id = Column(Integer, ForeignKey("bikes.id"), nullable=False)
    posted = Column(Boolean, nullable=False)
