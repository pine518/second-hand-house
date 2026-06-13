from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.house_crud import get_house, list_filter_options, list_houses
from app.services.analysis_service import summary_metrics

router = APIRouter(tags=["页面"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render homepage with summary metrics."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "metrics": summary_metrics(db), "active": "home"},
    )


@router.get("/houses", response_class=HTMLResponse)
def house_list(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=60),
    city: str | None = None,
    district: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_area: float | None = None,
    max_area: float | None = None,
    room_count: int | None = None,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Render searchable house listing page."""
    result = list_houses(
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
    filters = {
        "city": city,
        "district": district,
        "min_price": min_price,
        "max_price": max_price,
        "min_area": min_area,
        "max_area": max_area,
        "room_count": room_count,
    }
    prev_query = _page_query(filters, result["page_size"], result["page"] - 1)
    next_query = _page_query(filters, result["page_size"], result["page"] + 1)
    return templates.TemplateResponse(
        "house_list.html",
        {
            "request": request,
            "result": result,
            "filters": filters,
            "options": list_filter_options(db),
            "prev_query": prev_query,
            "next_query": next_query,
            "active": "houses",
        },
    )


@router.get("/houses/{house_id}", response_class=HTMLResponse)
def house_detail(
    house_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Render house detail page."""
    house = get_house(db, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="房源不存在")
    return templates.TemplateResponse(
        "house_detail.html",
        {"request": request, "house": house, "active": "houses"},
    )


@router.get("/analysis", response_class=HTMLResponse)
def analysis(request: Request) -> HTMLResponse:
    """Render visual analysis page."""
    return templates.TemplateResponse(
        "analysis.html",
        {"request": request, "active": "analysis"},
    )


def _page_query(filters: dict[str, object], page_size: int, page: int) -> str:
    """Build pagination query string while preserving active filters."""
    params = {
        key: value
        for key, value in filters.items()
        if value is not None and value != ""
    }
    params["page"] = max(page, 1)
    params["page_size"] = page_size
    return urlencode(params)
