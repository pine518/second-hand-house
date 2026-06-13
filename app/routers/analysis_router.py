from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.analysis_service import (
    area_price_scatter,
    avg_price_by_district,
    count_by_district,
    price_range,
    summary_metrics,
)

router = APIRouter(prefix="/api/analysis", tags=["数据分析 API"])


@router.get("/summary")
def api_summary(db: Session = Depends(get_db)) -> dict[str, float | int]:
    """Return dashboard summary metrics."""
    return summary_metrics(db)


@router.get("/avg-price-by-district")
def api_avg_price_by_district(
    city: str | None = None,
    db: Session = Depends(get_db),
) -> dict[str, list]:
    """Return average unit price by district."""
    return avg_price_by_district(db, city=city)


@router.get("/count-by-district")
def api_count_by_district(
    city: str | None = None,
    db: Session = Depends(get_db),
) -> dict[str, list[dict]]:
    """Return house count by district."""
    return count_by_district(db, city=city)


@router.get("/price-range")
def api_price_range(
    city: str | None = None,
    db: Session = Depends(get_db),
) -> dict[str, list]:
    """Return total price distribution."""
    return price_range(db, city=city)


@router.get("/area-price-scatter")
def api_area_price_scatter(
    city: str | None = None,
    db: Session = Depends(get_db),
) -> dict[str, list]:
    """Return area and price scatter points."""
    return area_price_scatter(db, city=city)
