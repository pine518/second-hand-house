from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HouseBase(BaseModel):
    """Shared house listing fields."""

    title: str
    city: str
    district: str | None = None
    community: str | None = None
    total_price: float | None = None
    unit_price: float | None = None
    area: float | None = None
    room_count: int | None = None
    hall_count: int | None = None
    floor: str | None = None
    orientation: str | None = None
    decoration: str | None = None
    build_year: int | None = None
    source_url: str


class HouseCreate(HouseBase):
    """House listing payload used for creation."""


class HouseRead(HouseBase):
    """House listing response model."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    crawl_time: datetime | None = None
    created_at: datetime | None = None


class HouseListResponse(BaseModel):
    """Paginated house listing response."""

    items: list[HouseRead]
    total: int
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    pages: int
