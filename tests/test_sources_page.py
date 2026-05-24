from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_sources_page_reads_like_public_source_overview() -> None:
    content = (ROOT / "dashboard" / "sources.html").read_text(encoding="utf-8")
    assert "資料來源" in content
    assert "資料來源總覽" in content
    assert "已有原型資料" in content
    assert "官方資料來源盤點" in content
    assert "未來要接入的資料" in content
    assert "prototype dashboard" in content
    assert "非正式全量資料" in content
    assert "no live crawler" in content
    assert "no source_url requests" in content
    assert "no personal data" in content
    assert "approved_for_crawling" in content


def test_sources_page_keeps_public_navigation_links() -> None:
    content = (ROOT / "dashboard" / "sources.html").read_text(encoding="utf-8")
    for link in [
        "./index.html",
        "./command-center.html",
        "./open-data-inventory.html",
        "./methodology.html",
        "./health-check.html",
        "./source-verification-workspace.html",
    ]:
        assert link in content
