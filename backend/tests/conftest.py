import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from database import Base
from models import User
from main import app
from security import passwords

@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(engine):
    TestingSession = sessionmaker(bind=engine, expire_on_commit=False)
    with TestingSession() as session:
        yield session

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
