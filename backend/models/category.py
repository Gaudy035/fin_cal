from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "t_category"

    category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_name = Column(String(30), unique=True, nullable=False)
    
    transactions_fk = relationship("Transaction", back_populates="category_fk")
    recurring_fk = relationship("Recurring", back_populates="category_fk")