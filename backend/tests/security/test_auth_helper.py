import security.auth as auth
from security.auth import SECRET_KEY, ALGORITHM
from models import User
from fastapi import status, HTTPException
import pytest
import jwt

def test_create_access_token_create_valid_token():
    token_dict = {
        "sub": "42"
    }

    result = auth.create_access_token(token_dict)
    decoded_token = jwt.decode(result, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == "42"

def test_get_current_user_with_correct_token_returns_user(db_session, seed_user):
    user: User = seed_user()
    token = auth.create_access_token({"sub": str(user.user_id)})
    result = auth.get_current_user(token, db_session)

    assert result == user

def test_get_current_user_with_token_sub_none_raises_401(db_session, seed_user):
    token_dict = {
        "sub": None
    }
    token = auth.create_access_token(token_dict)

    with pytest.raises(HTTPException) as result:
        auth.get_current_user(token, db_session)

    assert result.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user_with_invalid_token_raises_401(db_session, seed_user):
    with pytest.raises(HTTPException) as result:
        auth.get_current_user("invalid_token", db_session)

    assert result.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user_with_invalid_id_raises_401(db_session, seed_user):
    token = auth.create_access_token({"sub": "42"})

    with pytest.raises(HTTPException) as result:
        auth.get_current_user(token, db_session)

    assert result.value.status_code == status.HTTP_401_UNAUTHORIZED