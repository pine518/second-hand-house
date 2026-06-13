from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.house import House


def avg_price_by_district(db: Session, city: str | None = None) -> dict[str, list]:
    """Calculate average unit price grouped by district."""
    query = (
        select(House.district, func.avg(House.unit_price))
        .where(House.district.is_not(None), House.unit_price.is_not(None))
        .group_by(House.district)
        .order_by(func.avg(House.unit_price).desc())
    )
    if city:
        query = query.where(House.city == city)
    rows = db.execute(query).all()
    return {
        "labels": [row[0] for row in rows],
        "values": [round(float(row[1] or 0), 2) for row in rows],
    }


def count_by_district(db: Session, city: str | None = None) -> dict[str, list[dict]]:
    """Count house listings grouped by district."""
    query = (
        select(House.district, func.count(House.id))
        .where(House.district.is_not(None))
        .group_by(House.district)
        .order_by(func.count(House.id).desc())
    )
    if city:
        query = query.where(House.city == city)
    rows = db.execute(query).all()
    return {"items": [{"name": row[0], "value": int(row[1])} for row in rows]}


def price_range(db: Session, city: str | None = None) -> dict[str, list]:
    """Calculate total price distribution in common house-price ranges."""
    ranges = [
        ("100万以下", None, 100),
        ("100-200万", 100, 200),
        ("200-300万", 200, 300),
        ("300-500万", 300, 500),
        ("500-800万", 500, 800),
        ("800万以上", 800, None),
    ]
    labels: list[str] = []
    values: list[int] = []
    for label, lower, upper in ranges:
        query = select(func.count(House.id)).where(House.total_price.is_not(None))
        if city:
            query = query.where(House.city == city)
        if lower is not None:
            query = query.where(House.total_price >= lower)
        if upper is not None:
            query = query.where(House.total_price < upper)
        labels.append(label)
        values.append(int(db.scalar(query) or 0))
    return {"labels": labels, "values": values}


def area_price_scatter(db: Session, city: str | None = None) -> dict[str, list]:
    """Return area and total price points for scatter charts."""
    query = select(
        House.area,
        House.total_price,
        House.district,
        House.title,
    ).where(House.area.is_not(None), House.total_price.is_not(None))
    if city:
        query = query.where(House.city == city)
    rows = db.execute(query.limit(500)).all()
    return {
        "items": [
            {
                "area": float(row[0]),
                "total_price": float(row[1]),
                "district": row[2],
                "title": row[3],
            }
            for row in rows
        ]
    }


def summary_metrics(db: Session) -> dict[str, float | int]:
    """Return homepage summary metrics."""
    total = int(db.scalar(select(func.count(House.id))) or 0)
    avg_unit_price = db.scalar(select(func.avg(House.unit_price)))
    avg_total_price = db.scalar(select(func.avg(House.total_price)))
    district_count = int(
        db.scalar(select(func.count(func.distinct(House.district)))) or 0
    )
    return {
        "total": total,
        "avg_unit_price": round(float(avg_unit_price or 0), 2),
        "avg_total_price": round(float(avg_total_price or 0), 2),
        "district_count": district_count,
    }
