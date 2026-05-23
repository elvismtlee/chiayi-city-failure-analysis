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
