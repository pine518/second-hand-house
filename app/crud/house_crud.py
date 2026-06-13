from math import ceil

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.house import House


def build_house_query(
    city: str | None = None,
    district: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_area: float | None = None,
    max_area: float | None = None,
    room_count: int | None = None,
) -> Select[tuple[House]]:
    """Build a reusable filtered house query."""
    query = select(House)
    if city:
        query = query.where(House.city == city)
    if district:
        query = query.where(House.district == district)
    if min_price is not None:
        query = query.where(House.total_price >= min_price)
    if max_price is not None:
        query = query.where(House.total_price <= max_price)
    if min_area is not None:
        query = query.where(House.area >= min_area)
    if max_area is not None:
        query = query.where(House.area <= max_area)
    if room_count is not None:
        query = query.where(House.room_count == room_count)
    return query


def list_houses(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    city: str | None = None,
    district: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_area: float | None = None,
    max_area: float | None = None,
    room_count: int | None = None,
) -> dict[str, object]:
    """Return paginated house listings and pagination metadata."""
    page = max(page, 1)
    page_size = min(max(page_size, 1), 100)
    base_query = build_house_query(
        city=city,
        district=district,
        min_price=min_price,
        max_price=max_price,
        min_area=min_area,
        max_area=max_area,
        room_count=room_count,
    )
    total = db.scalar(select(func.count()).select_from(base_query.subquery())) or 0
    items = db.scalars(
        base_query.order_by(House.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": ceil(total / page_size) if total else 1,
    }


def get_house(db: Session, house_id: int) -> House | None:
    """Get one house listing by primary key."""
    return db.get(House, house_id)


def upsert_house(db: Session, payload: dict[str, object]) -> House:
    """Insert or update one house listing by source URL."""
    source_url = str(payload["source_url"])
    existing = db.scalar(select(House).where(House.source_url == source_url))
    if existing:
        for key, value in payload.items():
            setattr(existing, key, value)
        db.add(existing)
        return existing
    house = House(**payload)
    db.add(house)
    return house


def bulk_upsert_houses(db: Session, rows: list[dict[str, object]]) -> int:
    """Batch upsert cleaned house rows and return affected count."""
    count = 0
    for row in rows:
        if not row.get("source_url"):
            continue
        upsert_house(db, row)
        count += 1
    db.commit()
    return count


def list_filter_options(db: Session) -> dict[str, list[object]]:
    """Return distinct values used by page filter controls."""
    cities = db.scalars(select(House.city).distinct().order_by(House.city)).all()
    districts = db.scalars(
        select(House.district)
        .where(House.district.is_not(None))
        .distinct()
        .order_by(House.district)
    ).all()
    rooms = db.scalars(
        select(House.room_count)
        .where(House.room_count.is_not(None))
        .distinct()
        .order_by(House.room_count)
    ).all()
    return {"cities": cities, "districts": districts, "rooms": rooms}
