import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from database import Base
from models import User, Category, Transaction, Recurring
from security import passwords
from enums import TransactionMethod, TransactionType
from datetime import date, timedelta

@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(engine):
    testing_session = sessionmaker(bind=engine, expire_on_commit=False)
    with testing_session() as session:
        yield session

@pytest.fixture
def seed_category(db_session: Session):
    def _seed(name: str = "Food"):
        category = Category(category_name = name)
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)
        return category
    return _seed


@pytest.fixture
def seed_user(db_session: Session):
    def _seed(
        first_name: str = "John",
        last_name: str = "Doe",
        email: str = "john@example.com",
        password: str = "TestPass",
    ):
        hashed_pwd = passwords.hash_password(password)

        user = User(
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = hashed_pwd
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        return user
    return _seed

@pytest.fixture
def seed_transaction(db_session: Session):
    def _seed(
        user_id: int,
        category_id: int,
        amount: float = 100,
        transaction_type: TransactionType = TransactionType.EXPENSE,
        transaction_method: TransactionMethod = TransactionMethod.CASH,
        transaction_date: date = date.today()
    ):
        transaction = Transaction(
            user_id = user_id,
            category_id = category_id,
            title = "Seeded title",
            transaction_type = transaction_type,
            transaction_method = transaction_method,
            amount = amount,
            transaction_date = transaction_date
        )

        db_session.add(transaction)
        db_session.commit()
        db_session.refresh(transaction)

        return transaction
    return _seed

@pytest.fixture
def seed_recurring(db_session: Session):
    def _seed(
        user_id: int,
        category_id: int,
        amount: float = 100,
        transaction_type: TransactionType = TransactionType.EXPENSE,
        transaction_method: TransactionMethod = TransactionMethod.CASH,
        next_date: date = date.today() + timedelta(weeks=1),
        interval: str = "P30D"
    ):
        recurring = Recurring(
            user_id = user_id,
            category_id = category_id,
            title = "Seeded title",
            transaction_type = transaction_type,
            transaction_method = transaction_method,
            amount = amount,
            next_date = next_date,
            interval = interval
        )

        db_session.add(recurring)
        db_session.commit()
        db_session.refresh(recurring)

        return recurring
    return _seed