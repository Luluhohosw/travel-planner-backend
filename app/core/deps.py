from __future__ import annotations

from typing import Annotated
from fastapi import Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

DBSession = Annotated[AsyncSession, Depends(get_db)]


def get_api_key(x_api_key: str = Header(default="", alias="X-API-Key")) -> str:
    return x_api_key
