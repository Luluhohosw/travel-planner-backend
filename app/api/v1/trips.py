from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from app.core.deps import DBSession
from app.schemas.common import Response
from app.schemas.trip import TripCreate, TripUpdate, FieldUpdate
from app.services import trip_service

router = APIRouter()


@router.get("/trips")
async def list_trips(
    db: DBSession,
    search: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    result = await trip_service.get_all_trips(db, search, page, page_size)
    return Response(data=result)


@router.post("/trips")
async def create_trip(data: TripCreate, db: DBSession):
    tid = await trip_service.create_trip(db, data.model_dump())
    trip = await trip_service.get_trip_by_id(db, tid)
    return Response(data=trip, message="创建成功")


@router.get("/trips/{trip_id}")
async def get_trip(trip_id: int, db: DBSession):
    trip = await trip_service.get_trip_by_id(db, trip_id)
    if not trip:
        return Response(code=404, message="行程未找到", data=None)
    return Response(data=trip)


@router.put("/trips/{trip_id}")
async def update_trip(trip_id: int, data: TripUpdate, db: DBSession):
    ok = await trip_service.update_trip(db, trip_id, data.model_dump(exclude_none=True))
    if not ok:
        return Response(code=404, message="行程未找到", data=None)
    trip = await trip_service.get_trip_by_id(db, trip_id)
    return Response(data=trip, message="更新成功")


@router.delete("/trips/{trip_id}")
async def delete_trip(trip_id: int, db: DBSession):
    ok = await trip_service.delete_trip(db, trip_id)
    if not ok:
        return Response(code=404, message="行程未找到", data=None)
    return Response(message="删除成功")


@router.patch("/trips/{trip_id}/field")
async def update_field(trip_id: int, data: FieldUpdate, db: DBSession):
    ok = await trip_service.update_trip_field(db, trip_id, data.field, data.value)
    if not ok:
        return Response(code=404, message="行程未找到", data=None)
    return Response(message="更新成功")
