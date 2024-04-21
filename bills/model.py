from sqlalchemy import Boolean, Text, Column, Integer, String, DateTime, ForeignKey, Date
from database.database import Base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    price = Column(String(length=5), nullable=False)
    appointment_ids = Column(ARRAY(Integer))
    orders_ids = Column(ARRAY(Integer))
    document_title = Column(Text)
    bill_content = Column(Text)
