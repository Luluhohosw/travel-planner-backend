from __future__ import annotations

from pydantic import BaseModel, Field


class MemberCreate(BaseModel):
    name: str = Field(..., max_length=50)


class MembersSave(BaseModel):
    names: list[str]


class MemberResponse(BaseModel):
    id: int
    name: str
    role: str

    model_config = {"from_attributes": True}
