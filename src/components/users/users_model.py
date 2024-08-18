from dataclasses import dataclass


@dataclass
class User:

    id: str
    name: str

    password_hash: str
    password_salt: str