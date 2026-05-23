from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-top10-tasks.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_top10_tasks_page_exists_with_filters_and_safety_labels() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "Top 10 官方資料人工審核任務" in content
    assert 'id="openDataTop10Search"' in content
    assert 'id="openDataTop10TopicGroup"' in content
    assert 'id="openDataTop10Priority"' in content
    assert 'id="openDataTop10Status"' in content
    assert "manual review required" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_top10_review_tasks() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_top10_review_tasks.json" in content
    assert "setupOpenDataTop10Tasks" in content
    assert "openDataTop10Search" in content
    assert "openDataTop10Priority" in content
    assert "openDataTop10Status" in content
