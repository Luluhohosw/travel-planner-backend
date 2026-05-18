from __future__ import annotations

from fastapi import APIRouter, Depends
from app.core.deps import get_api_key
from app.schemas.common import Response
from app.schemas.ai import (
    ItineraryRequest, ChecklistRequest, DiscountRequest,
    DatesRequest, RoutesRequest, SuggestRequest,
)
from app.services import ai_planner

router = APIRouter()


@router.post("/ai/generate-itinerary")
async def generate_itinerary(data: ItineraryRequest, api_key: str = Depends(get_api_key)):
    result = await ai_planner.generate_itinerary(
        api_key=api_key,
        departure=data.departure,
        destination=data.destination,
        days=data.days,
        adults=data.adults,
        children=data.children,
        elders=data.elders,
        budget=data.budget,
        preferences=data.preferences,
        requirements=data.requirements,
        travel_date=data.travel_date,
    )
    if isinstance(result, dict) and "error" in result:
        return Response(code=500, message=result.get("error", "AI生成失败"), data=result)
    return Response(data=result)


@router.post("/ai/generate-checklist")
async def generate_checklist(data: ChecklistRequest, api_key: str = Depends(get_api_key)):
    result = await ai_planner.generate_checklist(
        api_key=api_key,
        destination=data.destination,
        days=data.days,
        travel_date=data.travel_date,
        has_children=data.has_children,
        has_elders=data.has_elders,
    )
    if isinstance(result, dict) and "error" in result:
        return Response(code=500, message=result.get("error", "AI生成失败"), data=result)
    return Response(data=result)


@router.post("/ai/search-discounts")
async def search_discounts(data: DiscountRequest, api_key: str = Depends(get_api_key)):
    result = await ai_planner.search_discounts(api_key=api_key, destination=data.destination, keyword=data.keyword)
    if isinstance(result, dict) and "error" in result:
        return Response(code=500, message=result.get("error", "AI搜索失败"), data=result)
    return Response(data=result)


@router.post("/ai/recommend-dates")
async def recommend_dates(data: DatesRequest, api_key: str = Depends(get_api_key)):
    result = await ai_planner.recommend_dates(api_key=api_key, destination=data.destination)
    if isinstance(result, dict) and "error" in result:
        return Response(code=500, message=result.get("error", "AI分析失败"), data=result)
    return Response(data=result)


@router.post("/ai/find-best-routes")
async def find_best_routes(data: RoutesRequest, api_key: str = Depends(get_api_key)):
    result = await ai_planner.find_best_routes(
        api_key=api_key,
        destination=data.destination,
        current_city=data.current_city,
        travel_date=data.travel_date,
        travelers=data.travelers,
        budget_level=data.budget_level,
    )
    if isinstance(result, dict) and "error" in result:
        return Response(code=500, message=result.get("error", "AI路线搜索失败"), data=result)
    return Response(data=result)


@router.post("/ai/suggest-trips")
async def suggest_trips(data: SuggestRequest, api_key: str = Depends(get_api_key)):
    result = await ai_planner.suggest_trips(api_key=api_key, query=data.query, current_city=data.current_city)
    if isinstance(result, dict) and "error" in result:
        return Response(code=500, message=result.get("error", "AI推荐失败"), data=result)
    return Response(data=result)
