from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-engineering-review.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_engineering_review_page_exists_with_filters_and_safety_labels() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "官方資料 Engineering Review Checklist" in content
    assert 'id="openDataEngineeringReviewSearch"' in content
    assert 'id="openDataEngineeringReviewTopicGroup"' in content
    assert 'id="openDataEngineeringReviewStatus"' in content
    assert 'id="openDataEngineeringReviewFetchMethod"' in content
    assert 'id="openDataEngineeringReviewSourceGate"' in content
    assert "manual review" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert "engineering_review_allowed" in content
    assert "crawler_execution_allowed" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_engineering_review_checklist() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_engineering_review_checklist.json" in content
    assert "setupOpenDataEngineeringReview" in content
    assert "openDataEngineeringReviewSearch" in content
    assert "openDataEngineeringReviewStatus" in content
    assert "openDataEngineeringReviewSourceGate" in content


def test_open_data_engineering_review_page_links_to_review_sessions() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-review-sessions.html" in content
    assert "進入人工審核執行工作台" in content


def test_open_data_engineering_review_page_links_to_evidence_pack() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-review-evidence.html" in content
    assert "查看審核證據包" in content


def test_open_data_engineering_review_page_links_to_manual_review_results() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-manual-review-results.html" in content
    assert "查看審核結果輸入表" in content
