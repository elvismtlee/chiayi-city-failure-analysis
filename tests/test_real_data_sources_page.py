from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard"


def test_sources_page_shows_real_data_pipeline_status() -> None:
    content = (DASHBOARD / "sources.html").read_text(encoding="utf-8")
    assert "真實資料管線狀態" in content
    assert "CYCC public records crawler" in content
    assert "data-pipeline=\"status\"" in content
    assert "data-pipeline=\"records\"" in content
    assert "./shared-nav.js?v=20260523-navux" in content
    assert ".nav{display:block" in content


def test_site_pages_loads_cycc_crawler_report() -> None:
    content = (DASHBOARD / "site-pages.js").read_text(encoding="utf-8")
    assert "renderCrawlerStatus" in content
    assert "./data/cycc_public_records_crawl_report.json" in content
    assert "尚未偵測到正式抓取報告" in content
    assert "internal metadata" in content
