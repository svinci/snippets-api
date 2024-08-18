import hashlib, uuid


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = uuid.uuid4().hex if salt is None else salt
    hashed_password = hashlib.sha512(
        (password + salt).encode()
    ).hexdigest()
    return hashed_password, salt
