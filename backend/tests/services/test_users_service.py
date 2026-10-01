import services.users as service
from models import User
from security import passwords, auth
import pytest
from fastapi import HTTPException, status
import schemas.user as schemas
from sqlalchemy.orm import Session

def test_register_user_with_correct_data_creates_and_returns_new_user(db_session):
    user_data = schemas.UserCreate(
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

    result = service.login_user(
        schemas.UserLogin(
            email = "john@example.com",
            password = "TestPass"
        ), db_session
    )

    assert auth.get_current_user(result["access_token"], db_session).user_id == user.user_id

def test_login_user_with_incorrect_email_raises_401(db_session, seed_user):
    seed_user()

    with pytest.raises(HTTPException) as result:
        service.login_user(
            schemas.UserLogin(
                email="jane@example.net",
                password="TestPass"
            ), db_session
        )

    assert result.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_login_user_with_incorrect_password_raises_401(db_session, seed_user):
    seed_user()

    with pytest.raises(HTTPException) as result:
        service.login_user(
            schemas.UserLogin(
                email="john@example.net",
                password="IncorrectPass"
            ), db_session
        )

    assert result.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_email_with_correct_data_changes_email(db_session: Session, seed_user):
    user: User = seed_user()

    assert user.email == "john@example.com"
    
    service.update_email(
        schemas.EmailChange(
            new_email="jane@example.com",
            current_password="TestPass"
        ), 
        user,
        db_session
    )

    assert user.email == "jane@example.com"

def test_update_email_with_taken_email_raises_409(db_session: Session, seed_user):
    user = seed_user()
    seed_user(
        first_name = "Jane",
        last_name = "Doe",
        email = "jane@example.com",
        password = "TestPass2",
    )

    with pytest.raises(HTTPException) as result:
        service.update_email(
            schemas.EmailChange(
                new_email="jane@example.com",
                current_password="TestPass"
            ), 
            user,
            db_session
        )

    assert result.value.status_code == status.HTTP_409_CONFLICT

def test_update_email_with_incorrect_password_raises_401(db_session: Session, seed_user):
    user = seed_user()

    with pytest.raises(HTTPException) as result:
        service.update_email(
            schemas.EmailChange(
                new_email="jane@example.com",
                current_password="IncorrectPass"
            ), 
            user,
            db_session
        )

    assert result.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_passwrod_with_correct_data_changes_password(db_session, seed_user):
    user: User = seed_user()

    assert passwords.verify_password("TestPass", user.password)

    service.update_password(
        schemas.PasswordChange(
            current_password="TestPass",
            new_password="NewPass"
        ),
        user,
        db_session
    )

    assert not passwords.verify_password("TestPass", user.password)
    assert passwords.verify_password("NewPass", user.password)

def test_update_passwrod_with_incorrect_current_password_raises_401(db_session, seed_user):
    user = seed_user()

    with pytest.raises(HTTPException) as result:
        service.update_password(
            schemas.PasswordChange(
                current_password="IncorrectPass",
                new_password="NewPass"
            ),
            user,
            db_session
        )

    assert result.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_user_with_correct_password_deletes_user(db_session: Session, seed_user):
    user: User = seed_user()

    schema = schemas.UserDelete(
        password = "TestPass"
    )

    user_id = user.user_id

    service.delete_user(schema, user, db_session)

    deleted_user = db_session.get(User, user_id)

    assert deleted_user is None

def test_delete_user_with_incorrect_password_does_not_delete_and_raises_401(db_session: Session, seed_user):
    user: User = seed_user()

    schema = schemas.UserDelete(
        password = "IncorrectPassword"
    )

    user_id = user.user_id

    with pytest.raises(HTTPException) as result:
        service.delete_user(schema, user, db_session)

    assert result.value.status_code == status.HTTP_401_UNAUTHORIZED

    user_refetch = db_session.get(User, user_id)

    assert user_refetch is not None