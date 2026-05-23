from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-manual-review-patches.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_manual_review_patches_page_exists_with_required_sections() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "人工審核結果回填 Patch 草稿" in content
    assert "openDataManualReviewPatches" in content
    assert "patch_status" in content
    assert "review_day" in content
    assert "topic_group" in content
    assert "manual review" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert "crawler_execution_allowed" in content
    assert "engineering_review_allowed" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_manual_review_patches() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_manual_review_result_patch_drafts.json" in content
    assert "setupOpenDataManualReviewPatches" in content
    assert "openDataManualReviewPatchDay" in content


def test_open_data_manual_review_patches_links_to_day1_sample_results() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-day1-sample-results.html" in content
    assert "查看 Day1 填寫範例" in content
