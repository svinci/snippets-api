from src.infrastructure.model import APIError
from cryptography.hazmat.primitives import serialization 
import jwt

def decode_jwt(token: str, public_key_path: str, algorithm: str) -> dict:
    sshkey = _load_public_key(public_key_path)
    return _decode_jwt(token, sshkey, algorithm)

def encode_jwt(payload: dict, private_key_path: str, key_pass: str, algorithm: str) -> str:
    sshkey = _load_private_key(private_key_path, key_pass)
    return _encode_jwt(payload, sshkey, algorithm)

def _decode_jwt(token: str, sshkey: serialization.SSHPublicKeyTypes, algorithm: str) -> dict:
    try:
        return jwt.decode(
            jwt=token,
            key=sshkey,
            algorithms=[algorithm]
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise APIError('Expired token', 401)
    except jwt.exceptions.InvalidTokenError:
        raise APIError('Invalid token', 401)

def _encode_jwt(payload: dict, sshkey: serialization.SSHPrivateKeyTypes, algorithm: str) -> str:
    return jwt.encode(
        payload=payload,
        key=sshkey,
        algorithm=algorithm,
        
    )

def _load_public_key(public_key_path: str) -> serialization.SSHPublicKeyTypes:
    sshkey = open(public_key_path, 'r').read()
    return serialization.load_ssh_public_key(sshkey.encode())

def _load_private_key(private_key_path: str, key_pass: str) -> serialization.SSHPrivateKeyTypes:
    sshkey = open(private_key_path, 'r').read()
    return serialization.load_ssh_private_key(sshkey.encode(), password=key_pass.encode())
