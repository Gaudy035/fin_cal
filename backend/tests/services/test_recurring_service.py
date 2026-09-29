import services.recurring as service
from models import Category, Recurring, User
from datetime import date, timedelta
import schemas.recurring as schemas
from enums import TransactionMethod, TransactionType
from fastapi import HTTPException, status
import pytest

def test_add_recurring_with_correct_data_creates_and_returns_recurring(db_session, seed_category, seed_user):
    user: User = seed_user()
    category: Category = seed_category()

    recurring = schemas.RecurringCreate(
        user_id=user.user_id,
        category_id=category.category_id,
        title="Title",
        transaction_type=TransactionType.INCOME,
        amount=100,
        transaction_method=TransactionMethod.CASH,
        next_date=date.today() + timedelta(weeks=1),
        interval="P7D"
    )

    result:Recurring = service.add_recurring(recurring, db_session, user)

    assert result.user_id == recurring.user_id
    assert result.category_id == recurring.category_id
    assert result.amount == recurring.amount
    assert result.transaction_type == recurring.transaction_type
    assert result.transaction_method == recurring.transaction_method
    assert result.next_date == recurring.next_date
    assert result.interval == recurring.interval

def test_get_recurring_returns_all_recurring_of_current_user(db_session, seed_user, seed_category, seed_recurring):
    user: User = seed_user()
    result = service.get_recurring(user, db_session)

    assert len(result) == 0

    category: Category = seed_category()
    seed_recurring(
        user_id = user.user_id,
        category_id = category.category_id,
        amount = 100,
        transaction_type = TransactionType.INCOME,
        transaction_method = TransactionMethod.CASH,
    )
    seed_recurring(
        user_id = user.user_id,
        category_id = category.category_id,
        amount = 100,
        transaction_type = TransactionType.EXPENSE,
        transaction_method = TransactionMethod.TRANSFER,
    )

    user2: User = seed_user(
        first_name = "Jane",
        last_name = "Doe",
        email = "jane@example.com",
        password = "TestPass2",
    )

    seed_recurring(
        user_id = user2.user_id,
        category_id = category.category_id,
        amount = 100,
        transaction_type = TransactionType.EXPENSE,
        transaction_method = TransactionMethod.TRANSFER,
    )

    result = service.get_recurring(user, db_session)

    assert len(result) == 2

def test_modify_recurring_with_correct_data_modifies_recurring(db_session, seed_category, seed_user, seed_recurring):
    user: User = seed_user()
    category: Category = seed_category()
    recurring: Recurring = seed_recurring(
        user_id=user.user_id,
        category_id=category.category_id,
        amount = 100,
        transaction_type=TransactionType.INCOME,
        transaction_method=TransactionMethod.CASH,
    )

    assert recurring.is_active

    service.modify_recurring(
        recurring.recurring_id, 
        schemas.RecurringUpdate(
            user_id = recurring.user_id,
            category_id = recurring.category_id,
            transaction_type = recurring.transaction_type,
            title = recurring.title,
            description = recurring.description,
            amount = recurring.amount,
            transaction_method = recurring.transaction_method,
            account = recurring.account,
            account_owner = recurring.account_owner,
            interval = recurring.interval,
            next_date = recurring.next_date,
            is_active = False
        ), 
        user, 
        db_session
    )

    assert not recurring.is_active

def test_modify_recurring_with_incorrect_recurring_id_raises_404(db_session, seed_category, seed_user, seed_recurring):
    user: User = seed_user()
    category: Category = seed_category()
    recurring: Recurring = seed_recurring(
        user_id=user.user_id,
        category_id=category.category_id,
        amount = 100,
        transaction_type=TransactionType.INCOME,
        transaction_method=TransactionMethod.CASH,
    )

    with pytest.raises(HTTPException) as result:
        service.modify_recurring(
            42,
            schemas.RecurringUpdate(
                user_id = recurring.user_id,
                category_id = recurring.category_id,
                transaction_type = recurring.transaction_type,
                title = recurring.title,
                description = recurring.description,
                amount = recurring.amount,
                transaction_method = recurring.transaction_method,
                account = recurring.account,
                account_owner = recurring.account_owner,
                interval = recurring.interval,
                next_date = recurring.next_date,
                is_active = False
            ), 
            user, 
            db_session
        )

    assert result.value.status_code == status.HTTP_404_NOT_FOUND