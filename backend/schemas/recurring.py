from pydantic import BaseModel, ConfigDict
from datetime import date
from enums import TransactionType, TransactionMethod

class RecurringBase(BaseModel):
    user_id: int | None = None
    category_id: int | None = None
    transaction_type: TransactionType
    title: str
    description: str | None = None
    amount: float
    transaction_method: TransactionMethod
    account: str | None = None
    account_owner: str | None = None
    interval: str
    next_date: date

class RecurringCreate(RecurringBase):
    pass
    
class RecurringResponse(RecurringBase):
    recurring_id: int
    is_active: bool
    model_config = ConfigDict(from_attributes = True)

class RecurringUpdate(RecurringBase):
    is_active: bool