from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def utc_now() -> datetime:
    """Return a naive UTC datetime for MySQL DATETIME columns."""
    return datetime.now(UTC).replace(tzinfo=None)


class House(Base):
    """Second-hand house listing persisted after crawling and cleaning."""

    __tablename__ = "house"
    __table_args__ = (
        Index("uq_house_source_url", "source_url", unique=True),
        Index("idx_house_city_district", "city", "district"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(64), nullable=False)
    district: Mapped[str | None] = mapped_column(String(64))
    community: Mapped[str | None] = mapped_column(String(128))
    total_price: Mapped[float | None] = mapped_column(Float)
    unit_price: Mapped[float | None] = mapped_column(Float)
    area: Mapped[float | None] = mapped_column(Float)
    room_count: Mapped[int | None] = mapped_column(Integer)
    hall_count: Mapped[int | None] = mapped_column(Integer)
    floor: Mapped[str | None] = mapped_column(String(64))
    orientation: Mapped[str | None] = mapped_column(String(64))
    decoration: Mapped[str | None] = mapped_column(String(64))
    build_year: Mapped[int | None] = mapped_column(Integer)
    source_url: Mapped[str] = mapped_column(String(768), nullable=False)
    crawl_time: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
