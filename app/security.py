import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, status
from .config import get_settings

ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310_000)
    return f"pbkdf2_sha256$310000${salt.hex()}${digest.hex()}"

def verify_password(password: str, encoded: str) -> bool:
    try:
        scheme, rounds, salt_hex, digest_hex = encoded.split("$")
        if scheme != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(rounds))
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False

def create_access_token(user_id: int, email: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": str(user_id), "email": email, "iat": now, "exp": now + timedelta(minutes=get_settings().access_token_minutes)}
    return jwt.encode(payload, get_settings().secret_key, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, get_settings().secret_key, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc
