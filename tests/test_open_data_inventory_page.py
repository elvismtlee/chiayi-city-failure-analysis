from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-inventory.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_inventory_page_exists_with_controls_and_safety_labels() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "嘉義市官方開放資料 URL 盤點" in content
    assert "id=\"openDataSearch\"" in content
    assert "id=\"openDataTopicGroup\"" in content
    assert "internal / manual review required" in content
    assert "不啟動 crawler" in content
    assert "不抓個資" in content
    assert "no auto publish" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_inventory() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_url_inventory.json" in content
    assert "setupOpenDataInventory" in content
    assert "openDataSearch" in content
    assert "openDataTopicGroup" in content
    assert "traffic_parking" in content
