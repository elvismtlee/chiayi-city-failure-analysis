from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-human-review.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_human_review_page_exists_with_filters_and_safety_labels() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "官方資料人工審核工作簿" in content
    assert 'id="openDataHumanReviewSearch"' in content
    assert 'id="openDataHumanReviewTopicGroup"' in content
    assert 'id="openDataHumanReviewStatus"' in content
    assert 'id="openDataHumanReviewGate"' in content
    assert 'id="openDataHumanReviewFetchMethod"' in content
    assert "manual review" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert "engineering_review_allowed" in content
    assert "crawler_execution_allowed" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_human_review_workbook() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_human_review_workbook.json" in content
    assert "setupOpenDataHumanReview" in content
    assert "openDataHumanReviewSearch" in content
    assert "openDataHumanReviewGate" in content
    assert "openDataHumanReviewFetchMethod" in content


def test_open_data_human_review_page_links_to_engineering_review() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-engineering-review.html" in content
    assert "進入工程審查清單" in content
