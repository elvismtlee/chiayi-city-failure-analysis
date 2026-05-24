from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard"


def test_sources_page_keeps_public_entry_links() -> None:
    content = (DASHBOARD / "sources.html").read_text(encoding="utf-8")
    assert "./index.html" in content
    assert "./command-center.html" in content
    assert "./methodology.html" in content
    assert "資料來源" in content


def test_cycc_review_links_back_to_sources_page() -> None:
    content = (DASHBOARD / "cycc-review.html").read_text(encoding="utf-8")
    assert "./sources.html" in content
    assert "回資料來源與更新狀態" in content


def test_cycc_review_keeps_dashboard_home_escape_hatch() -> None:
    content = (DASHBOARD / "cycc-review.html").read_text(encoding="utf-8")
    assert "./index.html" in content
    assert "回儀表板首頁" in content
