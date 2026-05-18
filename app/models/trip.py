from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, autoincrement=True)
    departure = Column(String(100), nullable=False, default="")
    destination = Column(String(500), nullable=False, default="")
    travel_date = Column(String(200), default="")
    days = Column(Integer, nullable=False, default=1)
    adults = Column(Integer, default=1)
    children = Column(Integer, default=0)
    elders = Column(Integer, default=0)
    budget = Column(String(50), default="舒适型")
    preferences = Column(String(500), default="")
    requirements = Column(Text, default="")
    itinerary_json = Column(Text, default="")
    budget_json = Column(Text, default="")
    checklist_json = Column(Text, default="")
    status = Column(String(20), default="draft")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    members = relationship("TripMember", back_populates="trip", cascade="all, delete-orphan")
    expenses = relationship("TripExpense", back_populates="trip", cascade="all, delete-orphan")


class TripMember(Base):
    __tablename__ = "trip_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    name = Column(String(50), nullable=False)
    role = Column(String(20), default="member")

    trip = relationship("Trip", back_populates="members")


class TripExpense(Base):
    __tablename__ = "trip_expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    category = Column(String(50), nullable=False)
    item_name = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False, default=0)
    paid_by = Column(String(50), default="")
    note = Column(Text, default="")

    trip = relationship("Trip", back_populates="expenses")
