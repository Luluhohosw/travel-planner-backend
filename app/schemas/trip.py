from __future__ import annotations

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class TripCreate(BaseModel):
    departure: str = Field(default="", max_length=100)
    destination: str = Field(default="", max_length=500)
    travel_date: str = Field(default="", max_length=200)
    days: int = Field(default=1, ge=1, le=365)
    adults: int = Field(default=1, ge=1, le=100)
    children: int = Field(default=0, ge=0, le=50)
    elders: int = Field(default=0, ge=0, le=50)
    budget: str = Field(default="舒适型")
    preferences: str = Field(default="[]")
    requirements: str = Field(default="", max_length=2000)
    status: Literal["draft", "planning", "confirmed", "completed"] = Field(default="draft")


class TripUpdate(BaseModel):
    departure: str | None = Field(default=None, max_length=100)
    destination: str | None = Field(default=None, max_length=500)
    travel_date: str | None = Field(default=None, max_length=200)
    days: int | None = Field(default=None, ge=1, le=365)
    adults: int | None = Field(default=None, ge=1, le=100)
    children: int | None = Field(default=None, ge=0, le=50)
    elders: int | None = Field(default=None, ge=0, le=50)
    budget: str | None = Field(default=None)
    preferences: str | None = Field(default=None)
    requirements: str | None = Field(default=None, max_length=2000)
    itinerary_json: str | None = Field(default=None)
    budget_json: str | None = Field(default=None)
    checklist_json: str | None = Field(default=None)
    status: Literal["draft", "planning", "confirmed", "completed"] | None = Field(default=None)


class TripResponse(BaseModel):
    id: int
    departure: str
    destination: str
    travel_date: str
    days: int
    adults: int
    children: int
    elders: int
    budget: str
    preferences: str
    requirements: str
    itinerary_json: str
    budget_json: str
    checklist_json: str
    status: str
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class TripList(BaseModel):
    id: int
    departure: str
    destination: str
    travel_date: str
    days: int
    people_count: int
    budget: str
    status: str
    created_at: str


class FieldUpdate(BaseModel):
    field: str
    value: str
