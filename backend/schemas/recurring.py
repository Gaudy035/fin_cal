from pydantic import BaseModel, ConfigDict
from datetime import date

class RecurringBase(BaseModel):
    user_id:int | None = None
    category_id:int | None = None
    transaction_type:str
    title:str
    description:str | None = None
    amount:float
    transaction_method:str
    account:str | None = None
    account_owner:str | None = None
    interval:str
    next_date:date

class RecurringCreate(RecurringBase):
    pass
    
class RecurringResponse(RecurringBase):
    recurring_id:int
    is_active:bool
    model_config = ConfigDict(from_attributes=True)

class RecurringUpdate(RecurringBase):
    is_active:bool