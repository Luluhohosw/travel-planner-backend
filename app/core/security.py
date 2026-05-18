from __future__ import annotations

from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 720


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return None
