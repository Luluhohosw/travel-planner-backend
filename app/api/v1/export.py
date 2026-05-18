from __future__ import annotations

import json
from fastapi import APIRouter, Depends
from app.core.deps import DBSession
from app.schemas.common import Response
from app.services import export_service, trip_service

router = APIRouter()


@router.get("/trips/{trip_id}/export/markdown")
async def export_markdown(trip_id: int, db: DBSession):
    trip = await trip_service.get_trip_by_id(db, trip_id)
    if not trip:
        return Response(code=404, message="行程未找到", data=None)
    md = export_service.itinerary_to_markdown(trip)
    return Response(data={"content": md, "filename": f"{trip['destination']}_旅行计划.md"})


@router.get("/trips/{trip_id}/export/json")
async def export_json(trip_id: int, db: DBSession):
    trip = await trip_service.get_trip_by_id(db, trip_id)
    if not trip:
        return Response(code=404, message="行程未找到", data=None)
    itinerary = json.loads(trip.get("itinerary_json") or "{}")
    return Response(data=itinerary)
