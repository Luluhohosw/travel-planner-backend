from __future__ import annotations

from fastapi import APIRouter, Depends
from app.core.deps import DBSession
from app.schemas.common import Response
from app.schemas.expense import ExpenseCreate
from app.services import trip_service

router = APIRouter()


@router.get("/trips/{trip_id}/expenses")
async def list_expenses(trip_id: int, db: DBSession):
    expenses = await trip_service.get_expenses(db, trip_id)
    return Response(data=expenses)


@router.post("/trips/{trip_id}/expenses")
async def add_expense(trip_id: int, data: ExpenseCreate, db: DBSession):
    eid = await trip_service.add_expense(db, trip_id, data.model_dump())
    return Response(data={"id": eid}, message="添加成功")


@router.delete("/trips/{trip_id}/expenses/{expense_id}")
async def remove_expense(trip_id: int, expense_id: int, db: DBSession):
    ok = await trip_service.delete_expense(db, trip_id, expense_id)
    if not ok:
        return Response(code=404, message="费用记录未找到", data=None)
    return Response(message="删除成功")


@router.get("/trips/{trip_id}/expenses/aa")
async def calculate_aa(trip_id: int, db: DBSession):
    members = await trip_service.get_members(db, trip_id)
    names = [m["name"] for m in members]
    if not names:
        return Response(code=400, message="请先保存成员", data=None)
    result = await trip_service.calculate_aa(db, trip_id, names)
    return Response(data=result)
