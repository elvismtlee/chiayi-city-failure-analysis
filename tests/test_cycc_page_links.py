from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard"


def test_sources_links_to_cycc_review_page() -> None:
    content = (DASHBOARD / "sources.html").read_text(encoding="utf-8")
    assert "./cycc-review.html" in content
    assert "前往 CYCC 公開資料審核" in content


def test_cycc_review_links_back_to_sources_page() -> None:
    content = (DASHBOARD / "cycc-review.html").read_text(encoding="utf-8")
    assert "./sources.html" in content
    assert "回資料來源與更新狀態" in content


def test_link_buttons_keep_dashboard_home_escape_hatch() -> None:
    for page in ["sources.html", "cycc-review.html"]:
        content = (DASHBOARD / page).read_text(encoding="utf-8")
        assert "./index.html" in content
        assert "回儀表板首頁" in content
