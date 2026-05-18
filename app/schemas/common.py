from __future__ import annotations

from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: T | None = None


class PaginatedData(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int
