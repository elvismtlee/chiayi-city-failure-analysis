from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-manual-review-results.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_manual_review_results_page_exists_with_filters_and_safety_labels() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "官方資料人工審核結果輸入表" in content
    assert 'id="openDataManualReviewResultSearch"' in content
    assert 'id="openDataManualReviewResultDay"' in content
    assert 'id="openDataManualReviewResultBatch"' in content
    assert 'id="openDataManualReviewResultStatus"' in content
    assert 'id="openDataManualReviewResultDecision"' in content
    assert 'id="openDataManualReviewResultTopicGroup"' in content
    assert "manual review" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert "crawler_execution_allowed" in content
    assert "engineering_review_allowed" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_manual_review_result_template() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_manual_review_result_template.json" in content
    assert "setupOpenDataManualReviewResults" in content
    assert "openDataManualReviewResultSearch" in content
    assert "openDataManualReviewResultDay" in content
    assert "openDataManualReviewResultBatch" in content


def test_open_data_manual_review_results_links_to_manual_review_sop() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-manual-review-sop.html" in content
    assert "查看人工審核 SOP" in content


def test_open_data_manual_review_results_links_to_manual_review_packets() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-manual-review-packets.html" in content
    assert "查看人工審核工作包" in content
