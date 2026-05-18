from __future__ import annotations

from fastapi import APIRouter, Depends
from app.core.deps import DBSession
from app.schemas.common import Response
from app.schemas.member import MembersSave
from app.services import trip_service

router = APIRouter()


@router.get("/trips/{trip_id}/members")
async def list_members(trip_id: int, db: DBSession):
    members = await trip_service.get_members(db, trip_id)
    return Response(data=members)


@router.put("/trips/{trip_id}/members")
async def save_members(trip_id: int, data: MembersSave, db: DBSession):
    await trip_service.save_members(db, trip_id, data.names)
    members = await trip_service.get_members(db, trip_id)
    return Response(data=members, message=f"成员已保存 ({len(data.names)}人)")
