from __future__ import annotations

from fastapi import APIRouter, Depends
from app.core.deps import get_api_key
from app.schemas.common import Response

router = APIRouter()


@router.post("/auth/wechat-login")
async def wechat_login(code: str = "", api_key: str = Depends(get_api_key)):
    """微信登录（占位，后续接入微信 code2session）"""
    return Response(data={"token": "", "openid": ""}, message="微信登录暂未接入，请使用API Key模式")


@router.get("/auth/me")
async def get_me():
    return Response(data={"username": "guest"})
