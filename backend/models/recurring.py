from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Numeric, Date, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enums import TransactionType, TransactionMethod

class Recurring(Base):
    __tablename__ = "t_recurring"

    recurring_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    user_id = Column(Integer, ForeignKey("t_user.user_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("t_category.category_id", ondelete="CASCADE"))
    
    transaction_type = Column(Enum(TransactionType, name="recurring_type_enum"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    transaction_method = Column(Enum(TransactionMethod, name="recurring_method_enum"), nullable=False)
    account = Column(String(50), nullable=True)
    account_owner = Column(String(100), nullable=True)
    interval = Column(String(10))
    next_date = Column(Date)
    is_active = Column(Boolean, default=True)
    
    user_fk = relationship("User", back_populates='recurring_fk')
    category_fk = relationship("Category", back_populates="recurring_fk")
