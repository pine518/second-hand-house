from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.house_crud import get_house, list_houses
from app.schemas.house_schema import HouseListResponse, HouseRead

router = APIRouter(prefix="/api", tags=["房源 API"])


@router.get("/houses", response_model=HouseListResponse)
def api_list_houses(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    city: str | None = None,
    district: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_area: float | None = None,
    max_area: float | None = None,
    room_count: int | None = None,
    db: Session = Depends(get_db),
) -> dict[str, object]:
    """Return paginated house listings."""
    return list_houses(
        db,
        page=page,
        page_size=page_size,
        city=city,
        district=district,
        min_price=min_price,
        max_price=max_price,
        min_area=min_area,
        max_area=max_area,
        room_count=room_count,
    )


@router.get("/houses/{house_id}", response_model=HouseRead)
def api_get_house(house_id: int, db: Session = Depends(get_db)) -> object:
    """Return one house listing by ID."""
    house = get_house(db, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="房源不存在")
    return house
