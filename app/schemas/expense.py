from __future__ import annotations

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    category: str = Field(..., max_length=50)
    item_name: str = Field(..., max_length=200)
    amount: float = Field(..., gt=0)
    paid_by: str = Field(default="", max_length=50)
    note: str = Field(default="", max_length=500)


class ExpenseResponse(BaseModel):
    id: int
    category: str
    item_name: str
    amount: float
    paid_by: str
    note: str

    model_config = {"from_attributes": True}


class AABalance(BaseModel):
    name: str
    paid: float
    balance: float
    status: str  # "应收", "应付", "已平账"


class AACalculation(BaseModel):
    per_person: float
    total: float
    balances: list[AABalance]
    tip: str = "应收的人向应付的人收款即可"
