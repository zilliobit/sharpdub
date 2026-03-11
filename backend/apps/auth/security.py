# security.py
import os
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from core.config import settings
from typing import Optional

SECRET_KEY = settings.SECRET_KEY

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 5

REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


def create_access_token(*, sub: str, sid: str, exp: Optional[timedelta] = None) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": sub,
        "sid": sid,
        "iat": now,
        "exp": now + (
            exp or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        ),
        "iss": settings.APP_NAME.lower(),
        "aud": f"{settings.APP_NAME.lower()}-access",
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(*, sid: str, exp: Optional[timedelta] = None) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sid": sid,
        "iat": now,
        "exp": now + (
            exp or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        ),
        "iss": settings.APP_NAME.lower(),
        "aud": f"{settings.APP_NAME.lower()}-refresh",
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)