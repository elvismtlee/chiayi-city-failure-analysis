from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-review-sessions.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_review_sessions_page_exists_with_filters_and_safety_labels() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "官方資料人工審核執行工作台" in content
    assert 'id="openDataReviewSessionSearch"' in content
    assert 'id="openDataReviewSessionDay"' in content
    assert 'id="openDataReviewSessionBatch"' in content
    assert 'id="openDataReviewSessionStatus"' in content
    assert 'id="openDataReviewSessionTopicGroup"' in content
    assert "manual review" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert "crawler_execution_allowed" in content
    assert "engineering_review_allowed" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_review_session_planner() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_review_session_planner.json" in content
    assert "setupOpenDataReviewSessions" in content
    assert "openDataReviewSessionSearch" in content
    assert "openDataReviewSessionDay" in content
    assert "openDataReviewSessionBatch" in content


def test_open_data_review_sessions_page_links_to_evidence_pack() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-review-evidence.html" in content
    assert "建立審核證據包" in content
