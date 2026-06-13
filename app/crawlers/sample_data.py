from typing import Any


def sample_houses(city: str = "上海") -> list[dict[str, Any]]:
    """Return deterministic sample rows for local first-run verification."""
    districts = ["浦东", "徐汇", "静安", "闵行", "杨浦", "长宁"]
    rows: list[dict[str, Any]] = []
    for index in range(1, 121):
        district = districts[index % len(districts)]
        area = 58 + (index % 70)
        unit_price = 52000 + (index % 35) * 1300
        total_price = round(area * unit_price / 10000, 1)
        rows.append(
            {
                "title": f"{district}清新两居样例房源 {index}",
                "city": city,
                "district": district,
                "community": f"{district}绿庭小区",
                "total_price": f"{total_price}万",
                "unit_price": f"{unit_price}元/平",
                "area": f"{area}平米",
                "layout": f"{1 + index % 4}室{1 + index % 2}厅",
                "floor": ["低楼层", "中楼层", "高楼层"][index % 3],
                "orientation": ["南北", "朝南", "东西"][index % 3],
                "decoration": ["精装", "简装", "毛坯"][index % 3],
                "build_year": f"{2000 + index % 23}年",
                "source_url": f"https://example.com/house/{index}",
            }
        )
    return rows
