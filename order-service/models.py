# models.py

from sqlalchemy import Column, Integer, String, Float
from database import Base

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {'extend_existing': True}  # Add this line ✅

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    item = Column(String, index=True)
    quantity = Column(Integer)
    total_price = Column(Float)
