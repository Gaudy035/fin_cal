from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Numeric, Date, Text, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Recurring(Base):
    __tablename__ = "t_recurring"

    recurring_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    user_id = Column(Integer, ForeignKey("t_user.user_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("t_categry.category_id", ondelete="CASCADE"))
    
    transaction_type = Column(String(10), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    transaction_method = Column(String(10), nullable=False)
    account = Column(String(50), nullable=True)
    account_owner = Column(String(100), nullable=True)
    interval = Column(String(10))
    next_date = Column(Date)
    is_active = Column(Boolean, default=True)
    
    __table_args__ = (
        CheckConstraint(transaction_type.in_(['wplyw', 'wydatek']), name='recurring_type_constraint'),
        CheckConstraint(transaction_method.in_(['gotowka', 'przelew']), name='recurring_method_constraint')
    )
    
    user_fk = relationship("User", back_populates='recurring_fk')
    category_fk = relationship("Category", back_populates="recurring_fk")
