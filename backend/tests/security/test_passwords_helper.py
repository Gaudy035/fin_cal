import security.passwords as passwords

def test_hash_password_hashes():
    password = "TestPassword"
    result = passwords.hash_password(password)

    assert not result == password

def test_verify_password_with_correct_password_returns_true():
    password = "TestPassword"
    hashed_password = passwords.hash_password(password)

    result = passwords.verify_password(password, hashed_password)

    assert result == True

def test_verify_password_with_incorrect_password_returns_false():
    password = "TestPassword"
    hashed_password = passwords.hash_password("IncorrectPassword")

    result = passwords.verify_password(password, hashed_password)

    assert result == False