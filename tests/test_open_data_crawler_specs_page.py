from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-crawler-specs.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_crawler_specs_page_exists_with_filters_and_safety_labels() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "官方資料 Crawler Spec 草稿" in content
    assert 'id="openDataCrawlerSpecSearch"' in content
    assert 'id="openDataCrawlerSpecTopicGroup"' in content
    assert 'id="openDataCrawlerSpecStatus"' in content
    assert 'id="openDataCrawlerSpecFetchMethod"' in content
    assert 'id="openDataCrawlerSpecRisk"' in content
    assert "manual review required" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert "crawler_execution_allowed" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_crawler_spec_drafts() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_crawler_spec_drafts.json" in content
    assert "setupOpenDataCrawlerSpecs" in content
    assert "openDataCrawlerSpecSearch" in content
    assert "openDataCrawlerSpecStatus" in content
    assert "openDataCrawlerSpecFetchMethod" in content


def test_open_data_crawler_specs_page_links_to_human_review() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-human-review.html" in content
    assert "進入人工審核工作簿" in content


def test_open_data_crawler_specs_page_links_to_engineering_review() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-engineering-review.html" in content
    assert "查看工程審查清單" in content
