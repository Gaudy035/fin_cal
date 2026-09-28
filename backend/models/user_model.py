from database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "t_user"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    is_active = Column(Boolean, default=True)
    deleted_at = Column(TIMESTAMP, nullable=True)

    transactions_fk = relationship("TransactionModel", back_populates="user_fk")
    recurring_fk = relationship("RecurringModel", back_populates="user_fk")