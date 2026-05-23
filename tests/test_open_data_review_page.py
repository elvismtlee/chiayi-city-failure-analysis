from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-review.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_review_page_exists_with_filters_and_safety_labels() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "嘉義市官方資料 URL 人工審核佇列" in content
    assert 'id="openDataReviewSearch"' in content
    assert 'id="openDataReviewTopicGroup"' in content
    assert 'id="openDataReviewStatus"' in content
    assert 'id="openDataReviewPriority"' in content
    assert "manual review required" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_review_queue() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_url_review_queue.json" in content
    assert "setupOpenDataReviewQueue" in content
    assert "openDataReviewSearch" in content
    assert "openDataReviewStatus" in content
    assert "openDataReviewPriority" in content


def test_open_data_review_page_links_to_readiness() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-readiness.html" in content
    assert "查看 Readiness 評分" in content
