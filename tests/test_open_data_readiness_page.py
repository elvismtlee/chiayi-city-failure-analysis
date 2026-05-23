from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-readiness.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_readiness_page_exists_with_filters_and_safety_labels() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "官方資料來源 Readiness 評分" in content
    assert 'id="openDataReadinessSearch"' in content
    assert 'id="openDataReadinessTopicGroup"' in content
    assert 'id="openDataReadinessLevel"' in content
    assert 'id="openDataReadinessStage"' in content
    assert "manual review required" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_readiness_report() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_readiness_report.json" in content
    assert "setupOpenDataReadiness" in content
    assert "openDataReadinessSearch" in content
    assert "openDataReadinessLevel" in content
    assert "openDataReadinessStage" in content


def test_open_data_readiness_page_links_to_top10_tasks() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-top10-tasks.html" in content
    assert "產生 Top 10 審核任務" in content


def test_open_data_readiness_page_links_to_crawler_specs() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-crawler-specs.html" in content
    assert "查看 Crawler 規格草稿" in content
