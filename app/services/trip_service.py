from __future__ import annotations

from sqlalchemy import select, delete, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trip import Trip, TripMember, TripExpense

ALLOWED_FIELDS = {
    "departure", "destination", "travel_date", "days", "adults", "children",
    "elders", "budget", "preferences", "requirements", "itinerary_json",
    "budget_json", "checklist_json", "status",
}


async def get_all_trips(db: AsyncSession, search: str = "", page: int = 1, page_size: int = 20) -> dict:
    q = select(Trip).order_by(desc(Trip.created_at))
    count_q = select(func.count(Trip.id))
    if search:
        q = q.where(Trip.destination.contains(search))
        count_q = count_q.where(Trip.destination.contains(search))

    total = (await db.execute(count_q)).scalar() or 0
    offset = (page - 1) * page_size
    rows = (await db.execute(q.offset(offset).limit(page_size))).scalars().all()

    items = []
    for t in rows:
        items.append({
            "id": t.id,
            "departure": t.departure or "",
            "destination": t.destination or "",
            "travel_date": t.travel_date or "",
            "days": t.days,
            "people_count": (t.adults or 0) + (t.children or 0) + (t.elders or 0),
            "budget": t.budget or "",
            "status": t.status or "draft",
            "created_at": t.created_at.strftime("%Y-%m-%d %H:%M") if t.created_at else "",
        })

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": max(1, (total + page_size - 1) // page_size),
    }


async def get_trip_by_id(db: AsyncSession, trip_id: int) -> dict | None:
    trip = (await db.execute(select(Trip).where(Trip.id == trip_id))).scalar_one_or_none()
    if not trip:
        return None
    return {
        "id": trip.id,
        "departure": trip.departure or "",
        "destination": trip.destination or "",
        "travel_date": trip.travel_date or "",
        "days": trip.days,
        "adults": trip.adults or 0,
        "children": trip.children or 0,
        "elders": trip.elders or 0,
        "budget": trip.budget or "",
        "preferences": trip.preferences or "",
        "requirements": trip.requirements or "",
        "itinerary_json": trip.itinerary_json or "",
        "budget_json": trip.budget_json or "",
        "checklist_json": trip.checklist_json or "",
        "status": trip.status or "draft",
        "created_at": trip.created_at.strftime("%Y-%m-%d %H:%M") if trip.created_at else "",
        "updated_at": trip.updated_at.strftime("%Y-%m-%d %H:%M") if trip.updated_at else "",
    }


async def create_trip(db: AsyncSession, data: dict) -> int:
    trip = Trip(**{k: v for k, v in data.items() if k != "id"})
    db.add(trip)
    await db.commit()
    await db.refresh(trip)
    return trip.id


async def update_trip(db: AsyncSession, trip_id: int, data: dict) -> bool:
    trip = (await db.execute(select(Trip).where(Trip.id == trip_id))).scalar_one_or_none()
    if not trip:
        return False
    for key, value in data.items():
        if value is not None and hasattr(trip, key):
            setattr(trip, key, value)
    await db.commit()
    return True


async def delete_trip(db: AsyncSession, trip_id: int) -> bool:
    trip = (await db.execute(select(Trip).where(Trip.id == trip_id))).scalar_one_or_none()
    if not trip:
        return False
    await db.delete(trip)
    await db.commit()
    return True


async def update_trip_field(db: AsyncSession, trip_id: int, field: str, value: str) -> bool:
    if field not in ALLOWED_FIELDS:
        return False
    trip = (await db.execute(select(Trip).where(Trip.id == trip_id))).scalar_one_or_none()
    if not trip:
        return False
    setattr(trip, field, value)
    await db.commit()
    return True


# ── Members ──

async def get_members(db: AsyncSession, trip_id: int) -> list:
    rows = (await db.execute(select(TripMember).where(TripMember.trip_id == trip_id))).scalars().all()
    return [{"id": m.id, "name": m.name, "role": m.role} for m in rows]


async def save_members(db: AsyncSession, trip_id: int, names: list[str]):
    await db.execute(delete(TripMember).where(TripMember.trip_id == trip_id))
    for name in names:
        if name.strip():
            db.add(TripMember(trip_id=trip_id, name=name.strip()))
    await db.commit()


# ── Expenses ──

async def get_expenses(db: AsyncSession, trip_id: int) -> list:
    rows = (await db.execute(select(TripExpense).where(TripExpense.trip_id == trip_id))).scalars().all()
    return [{"id": e.id, "category": e.category, "item_name": e.item_name, "amount": e.amount, "paid_by": e.paid_by, "note": e.note} for e in rows]


async def add_expense(db: AsyncSession, trip_id: int, data: dict) -> int:
    exp = TripExpense(trip_id=trip_id, **data)
    db.add(exp)
    await db.commit()
    await db.refresh(exp)
    return exp.id


async def delete_expense(db: AsyncSession, trip_id: int, expense_id: int) -> bool:
    exp = (await db.execute(
        select(TripExpense).where(TripExpense.id == expense_id, TripExpense.trip_id == trip_id)
    )).scalar_one_or_none()
    if not exp:
        return False
    await db.delete(exp)
    await db.commit()
    return True


async def calculate_aa(db: AsyncSession, trip_id: int, member_names: list[str]) -> dict:
    rows = (await db.execute(select(TripExpense).where(TripExpense.trip_id == trip_id))).scalars().all()
    total = sum(e.amount for e in rows)
    per_person = total / len(member_names) if member_names else 0

    paid_map = {}
    for e in rows:
        paid_map[e.paid_by] = paid_map.get(e.paid_by, 0) + e.amount

    balances = []
    for name in member_names:
        paid = paid_map.get(name, 0)
        balance = paid - per_person
        if balance > 0.01:
            status = "应收"
        elif balance < -0.01:
            status = "应付"
        else:
            status = "已平账"
        balances.append({"name": name, "paid": round(paid, 2), "balance": round(balance, 2), "status": status})

    return {
        "per_person": round(per_person, 2),
        "total": round(total, 2),
        "balances": balances,
        "tip": "应收的人向应付的人收款即可",
    }
