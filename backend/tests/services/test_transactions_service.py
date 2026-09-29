import services.transactions as service
from models import Category, Transaction, User
from datetime import date
from sqlalchemy.orm import Session
import schemas.transaction as schemas
from enums import TransactionMethod, TransactionType

def test_add_transaction_with_correct_data_creates_and_returns_transaction(db_session, seed_category, seed_user):
    user: User = seed_user()
    category: Category = seed_category()

    transaction = schemas.TransactionCreate(
        user_id=user.user_id,
        category_id=category.category_id,
        title="Title",
        transaction_type=TransactionType.INCOME,
        amount=100,
        transaction_method=TransactionMethod.CASH,
        transaction_date=date.today()
    )

    result:Transaction = service.add_transaction(transaction, db_session, user)

    assert result.user_id == transaction.user_id
    assert result.category_id == transaction.category_id
    assert result.amount == transaction.amount
    assert result.transaction_type == transaction.transaction_type
    assert result.transaction_method == transaction.transaction_method
    assert result.transaction_date == transaction.transaction_date

def test_get_transactions_returns_all_transactions_of_current_user(db_session, seed_user, seed_category, seed_transaction):
    user: User = seed_user()
    result = service.get_transactions(user, db_session)

    assert len(result) == 0

    category: Category = seed_category()
    seed_transaction(
        user_id = user.user_id,
        category_id = category.category_id,
        amount = 100,
        transaction_type = TransactionType.INCOME,
        transaction_method = TransactionMethod.CASH,
        transaction_date = date.today()
    )
    seed_transaction(
        user_id = user.user_id,
        category_id = category.category_id,
        amount = 100,
        transaction_type = TransactionType.EXPENSE,
        transaction_method = TransactionMethod.TRANSFER,
        transaction_date = date.today()
    )

    user2 = seed_user(
        first_name = "Jane",
        last_name = "Doe",
        email = "jane@example.com",
        password = "TestPass2",
    )

    seed_transaction(
        user_id = user2.user_id,
        category_id = category.category_id,
        amount = 100,
        transaction_type = TransactionType.EXPENSE,
        transaction_method = TransactionMethod.TRANSFER,
        transaction_date = date.today()
    )

    result = service.get_transactions(user, db_session)

    assert len(result) == 2