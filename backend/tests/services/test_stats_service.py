from models import User, Transaction, Category
from enums import TransactionType, TransactionMethod
import services.stats as service

def test_get_stats_returns_proper_data(db_session, seed_category, seed_transaction, seed_user):
    user: User = seed_user()
    user2: User = seed_user(
        first_name = "Jane",
        last_name = "Doe",
        email = "jane@example.com",
        password = "TestPass2",
    )
    cat1: Category = seed_category()
    cat2: Category = seed_category(name = "Health")

    tr1: Transaction = seed_transaction(
        user_id = user.user_id,
        category_id = cat1.category_id,
        amount = 100,
        transaction_type = TransactionType.EXPENSE,
        transaction_method = TransactionMethod.CASH,
    )
    tr2: Transaction = seed_transaction(
        user_id = user.user_id,
        category_id = cat1.category_id,
        amount = 200,
        transaction_type = TransactionType.EXPENSE,
        transaction_method = TransactionMethod.TRANSFER,
    )
    tr3: Transaction = seed_transaction(
        user_id = user.user_id,
        category_id = cat2.category_id,
        amount = 300,
        transaction_type = TransactionType.INCOME,
        transaction_method = TransactionMethod.CASH,
    )
    tr4: Transaction = seed_transaction(
        user_id = user.user_id,
        category_id = cat2.category_id,
        amount = 400,
        transaction_type = TransactionType.EXPENSE,
        transaction_method = TransactionMethod.CASH,
    )
    seed_transaction(
        user_id = user2.user_id,
        category_id = cat2.category_id,
        amount = 400,
        transaction_type = TransactionType.EXPENSE,
        transaction_method = TransactionMethod.CASH,
    )

    resutlt = service.get_stats(user, db_session)

    assert len(resutlt) == 2

    stats = {x["category"]: x["amount"] for x in resutlt}
    assert stats == {
        cat1.category_name: tr1.amount + tr2.amount,
        cat2.category_name: tr4.amount
    }

def test_get_summary_returns_proper_data(db_session, seed_category, seed_transaction, seed_user):
    user: User = seed_user()
    user2: User = seed_user(
        first_name = "Jane",
        last_name = "Doe",
        email = "jane@example.com",
        password = "TestPass2",
    )
    cat1: Category = seed_category()
    cat2: Category = seed_category(name = "Health")

    tr1: Transaction = seed_transaction(
        user_id = user.user_id,
        category_id = cat1.category_id,
        amount = 100,
        transaction_type = TransactionType.INCOME,
        transaction_method = TransactionMethod.CASH,
    )
    tr2: Transaction = seed_transaction(
        user_id = user.user_id,
        category_id = cat1.category_id,
        amount = 200,
        transaction_type = TransactionType.EXPENSE,
        transaction_method = TransactionMethod.TRANSFER,
    )
    tr3: Transaction = seed_transaction(
        user_id = user.user_id,
        category_id = cat2.category_id,
        amount = 300,
        transaction_type = TransactionType.INCOME,
        transaction_method = TransactionMethod.CASH,
    )
    tr4: Transaction = seed_transaction(
        user_id = user.user_id,
        category_id = cat2.category_id,
        amount = 400,
        transaction_type = TransactionType.EXPENSE,
        transaction_method = TransactionMethod.CASH,
    )
    seed_transaction(
        user_id = user2.user_id,
        category_id = cat2.category_id,
        amount = 400,
        transaction_type = TransactionType.EXPENSE,
        transaction_method = TransactionMethod.CASH,
    )

    resutlt = service.get_summary(user, db_session)

    assert len(resutlt) == 2

    summary = {x["type"]: x["amount"] for x in resutlt}
    assert summary == {
        TransactionType.INCOME: tr1.amount + tr3.amount,
        TransactionType.EXPENSE: tr2.amount + tr4.amount
    }
