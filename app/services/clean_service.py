import re
from datetime import UTC, datetime
from typing import Any


def parse_number(value: Any) -> float | None:
    """Extract the first numeric value from mixed text."""
    if value is None:
        return None
    text = str(value).replace(",", "").strip()
    match = re.search(r"\d+(?:\.\d+)?", text)
    return float(match.group()) if match else None


def parse_total_price(value: Any) -> float | None:
    """Parse total price in ten-thousand yuan units."""
    number = parse_number(value)
    if number is None or number <= 0:
        return None
    return number


def parse_unit_price(value: Any) -> float | None:
    """Parse unit price in yuan per square meter."""
    number = parse_number(value)
    if number is None or number <= 0:
        return None
    return number


def parse_area(value: Any) -> float | None:
    """Parse house area in square meters."""
    number = parse_number(value)
    if number is None or number <= 0:
        return None
    return number


def parse_layout(value: Any) -> tuple[int | None, int | None]:
    """Parse Chinese room layout text into room and hall counts."""
    if not value:
        return None, None
    text = str(value)
    match = re.search(r"(\d+)\s*室\s*(\d+)\s*厅", text)
    if match:
        return int(match.group(1)), int(match.group(2))
    room_match = re.search(r"(\d+)\s*室", text)
    hall_match = re.search(r"(\d+)\s*厅", text)
    room_count = int(room_match.group(1)) if room_match else None
    hall_count = int(hall_match.group(1)) if hall_match else None
    return room_count, hall_count


def parse_build_year(value: Any) -> int | None:
    """Parse a reasonable build year from text."""
    if not value:
        return None
    match = re.search(r"(19\d{2}|20\d{2})", str(value))
    if not match:
        return None
    year = int(match.group(1))
    current_year = datetime.now(UTC).year + 1
    return year if 1900 <= year <= current_year else None


def normalize_text(value: Any) -> str | None:
    """Normalize optional text fields."""
    if value is None:
        return None
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text or None


def clean_house(raw: dict[str, Any], default_city: str = "上海") -> dict[str, Any] | None:
    """Clean one raw crawler row into a database-ready house payload."""
    title = normalize_text(raw.get("title"))
    source_url = normalize_text(raw.get("source_url"))
    if not title or not source_url:
        return None

    room_count, hall_count = parse_layout(raw.get("layout") or raw.get("house_type"))
    total_price = parse_total_price(raw.get("total_price"))
    unit_price = parse_unit_price(raw.get("unit_price"))
    area = parse_area(raw.get("area"))

    if total_price is None and unit_price is not None and area is not None:
        total_price = round(unit_price * area / 10000, 2)
    if unit_price is None and total_price is not None and area is not None:
        unit_price = round(total_price * 10000 / area, 2)

    return {
        "title": title,
        "city": normalize_text(raw.get("city")) or default_city,
        "district": normalize_text(raw.get("district")),
        "community": normalize_text(raw.get("community")),
        "total_price": total_price,
        "unit_price": unit_price,
        "area": area,
        "room_count": room_count,
        "hall_count": hall_count,
        "floor": normalize_text(raw.get("floor")),
        "orientation": normalize_text(raw.get("orientation")),
        "decoration": normalize_text(raw.get("decoration")),
        "build_year": parse_build_year(raw.get("build_year")),
        "source_url": source_url,
        "crawl_time": datetime.now(UTC).replace(tzinfo=None),
    }


def clean_houses(rows: list[dict[str, Any]], default_city: str = "上海") -> list[dict[str, Any]]:
    """Clean a batch of raw crawler rows, skipping invalid records."""
    cleaned = []
    for row in rows:
        item = clean_house(row, default_city=default_city)
        if item:
            cleaned.append(item)
    return cleaned
