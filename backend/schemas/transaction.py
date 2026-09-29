from pydantic import BaseModel, ConfigDict
from datetime import date
from enums import TransactionType, TransactionMethod

class TransactionBase(BaseModel):
    user_id: int | None = None
    category_id: int | None = None
    transaction_type: TransactionType
    title: str
    description: str | None = None
    amount: float
    transaction_method: TransactionMethod
    account: str | None = None
    account_owner: str | None = None

class TransactionCreate(TransactionBase):
    transaction_date: date | None = None

class TransactionResponse(TransactionBase):
    transaction_id: int
    transaction_date: date
    model_config = ConfigDict(from_attributes = True)