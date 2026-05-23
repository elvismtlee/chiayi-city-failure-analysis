from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-day1-sample-results.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_day1_sample_results_page_exists_with_required_sections() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "Day 1 人工審核填寫範例" in content
    assert "openDataDay1SampleResults" in content
    assert "sample_only" in content
    assert "not_actual_review_result" in content
    assert "manual review" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert "crawler_execution_allowed" in content
    assert "engineering_review_allowed" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_day1_sample_results() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_day1_sample_manual_review_results.json" in content
    assert "setupOpenDataDay1SampleResults" in content
    assert "open-data-day1-sample-results" in content
