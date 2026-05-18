"""
FastAPI 入口 — 旅游规划助手微信小程序后端
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trip import Base
from app.core.database import engine, get_db
from app.api.v1 import trips, members, expenses, ai, export, theme, utils, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="旅游规划助手 API",
    description="微信小程序版旅游规划助手后端",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips.router, prefix="/api/v1", tags=["Trips"])
app.include_router(members.router, prefix="/api/v1", tags=["Members"])
app.include_router(expenses.router, prefix="/api/v1", tags=["Expenses"])
app.include_router(ai.router, prefix="/api/v1", tags=["AI"])
app.include_router(export.router, prefix="/api/v1", tags=["Export"])
app.include_router(theme.router, prefix="/api/v1", tags=["Theme"])
app.include_router(utils.router, prefix="/api/v1", tags=["Utils"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])


@app.get("/api/v1/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "error", "database": "disconnected"}
