from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-manual-review-packets.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_manual_review_packets_page_exists_with_required_sections() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "官方資料人工審核工作包" in content
    assert "openDataManualReviewPackets" in content
    assert "day_1" in content
    assert "day_2" in content
    assert "day_3" in content
    assert "manual review" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert "crawler_execution_allowed" in content
    assert "engineering_review_allowed" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_manual_review_packets() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_manual_review_execution_packets.json" in content
    assert "setupOpenDataManualReviewPackets" in content
    assert "open-data-manual-review-packets" in content


def test_open_data_manual_review_packets_links_to_patch_drafts() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-manual-review-patches.html" in content
    assert "建立回填 Patch 草稿" in content


def test_open_data_manual_review_packets_links_to_day1_review_form() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-day1-review-form.html" in content
    assert "查看 Day1 審核表單" in content
