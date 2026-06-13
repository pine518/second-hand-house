from app.crawlers.sample_data import sample_houses


def test_sample_houses_can_seed_first_run_data():
    """Sample data should be large enough to verify MVP pages and charts."""
    rows = sample_houses("上海")

    assert len(rows) == 120
    assert rows[0]["city"] == "上海"
    assert rows[0]["source_url"].startswith("https://example.com/house/")
