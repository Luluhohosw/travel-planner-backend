from __future__ import annotations

from pydantic import BaseModel, Field


class ItineraryRequest(BaseModel):
    departure: str
    destination: str
    days: int = Field(ge=1, le=365)
    adults: int = Field(default=1, ge=1, le=100)
    children: int = Field(default=0, ge=0, le=50)
    elders: int = Field(default=0, ge=0, le=50)
    budget: str = Field(default="舒适型")
    preferences: list[str] = Field(default_factory=list)
    requirements: str = Field(default="")
    travel_date: str = Field(default="")


class ChecklistRequest(BaseModel):
    destination: str
    days: int
    travel_date: str = ""
    has_children: bool = False
    has_elders: bool = False


class DiscountRequest(BaseModel):
    destination: str
    keyword: str


class DatesRequest(BaseModel):
    destination: str


class RoutesRequest(BaseModel):
    destination: str
    current_city: str = ""
    travel_date: str = ""
    travelers: int = Field(default=1, ge=1)
    budget_level: str = Field(default="舒适型")


class SuggestRequest(BaseModel):
    query: str
    current_city: str = ""
