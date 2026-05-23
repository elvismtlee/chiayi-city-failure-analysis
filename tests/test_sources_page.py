from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "sources.html"


def test_sources_page_links_to_open_data_inventory() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-inventory.html" in content
    assert "前往官方開放資料 URL 盤點" in content
