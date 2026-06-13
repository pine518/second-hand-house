from app.services.clean_service import clean_house, parse_area, parse_layout


def test_parse_area_extracts_square_meter_value():
    """Area parser should keep numeric square-meter value."""
    assert parse_area("89.5平米") == 89.5


def test_parse_layout_extracts_room_and_hall_counts():
    """Layout parser should parse Chinese room and hall counts."""
    assert parse_layout("3室2厅") == (3, 2)


def test_clean_house_returns_database_ready_payload():
    """Cleaned payload should contain numeric values and parsed layout."""
    row = {
        "title": "浦东 精装两居",
        "city": "上海",
        "district": "浦东",
        "community": "绿庭小区",
        "total_price": "320万",
        "unit_price": "60000元/平",
        "area": "53.3平米",
        "layout": "2室1厅",
        "build_year": "2015年",
        "source_url": "https://example.com/1",
    }

    cleaned = clean_house(row)

    assert cleaned is not None
    assert cleaned["total_price"] == 320
    assert cleaned["unit_price"] == 60000
    assert cleaned["area"] == 53.3
    assert cleaned["room_count"] == 2
    assert cleaned["hall_count"] == 1
    assert cleaned["build_year"] == 2015
