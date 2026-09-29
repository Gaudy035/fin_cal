import services.users as service
from models import User
from security import passwords, auth
import pytest
from fastapi import HTTPException, status
import schemas.user as schemas

def test_register_user_with_correct_data_creates_and_returns_new_user(db_session):
    user_data = User(
        first_name = "John",
        last_name = "Doe",
        email = "john@example.com",
        password = "TestPass",
    )

    result = service.register_user(user_data, db_session)
    
    assert result.first_name == user_data.first_name
    assert result.last_name == user_data.last_name
    assert result.email == user_data.email
    assert passwords.verify_password(user_data.password, result.password)

def test_register_user_with_duplicate_email_raises_409(db_session, seed_user):
    seed_user()
    user_data = User(
        first_name = "John",
        last_name = "Smith",
        email = "john@example.com",
        password = "TestPass2",
    )

    with pytest.raises(HTTPException) as result:
        service.register_user(user_data, db_session)

    assert result.value.status_code == status.HTTP_409_CONFLICT

def test_login_user_with_correct_credentials_return_correct_access_token(db_session, seed_user):
    user: User = seed_user()

    result = service.login_user(schemas.UserCreate(
        first_name = "John",
        last_name = "Doe",
        email = "john@example.com",
        password = "TestPass"
    ), db_session)

    assert auth.get_current_user(result["access_token"], db_session).user_id == user.user_id