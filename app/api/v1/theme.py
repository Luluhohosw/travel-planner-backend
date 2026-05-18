from __future__ import annotations

from fastapi import APIRouter, Query
from app.schemas.common import Response
from app.services.theme_service import get_season, get_colors, SEASON_DECOR, SEASONS

router = APIRouter()


@router.get("/theme/colors")
async def theme_colors(season: str = Query(default=""), month: int = Query(default=0)):
    s = season if season in SEASONS else get_season(month if month else None)
    colors = get_colors(s)
    decor = SEASON_DECOR.get(s, {})
    return Response(data={
        "season": s,
        "name": SEASONS[s]["name"],
        "colors": colors,
        "decor": decor,
    })


@router.get("/theme/seasons")
async def list_seasons():
    return Response(data=[
        {"key": k, "name": v["name"], "decor": SEASON_DECOR[k]}
        for k, v in SEASONS.items()
    ])
