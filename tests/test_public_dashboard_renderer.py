from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "dashboard" / "public-dashboard.js"
HOME = ROOT / "dashboard" / "index.html"


def test_public_dashboard_renderer_exists() -> None:
    assert JS.exists()


def test_public_dashboard_renderer_uses_local_dashboard_data() -> None:
    content = JS.read_text(encoding="utf-8")
    for text in [
        "safeText",
        "formatNumber",
        "loadJson",
        "renderHomepageKpis",
        "renderIssueRanking",
        "renderHotspotCards",
        "renderDataStatus",
        "initPublicDashboard",
        "./data/dashboard_summary.json",
        "./data/issue_trends.json",
        "./data/hotspots.json",
        "./data/dashboard_health_check.json",
        "./data/open_data_url_inventory.json",
    ]:
        assert text in content


def test_public_dashboard_renderer_has_no_external_fetch_targets() -> None:
    content = JS.read_text(encoding="utf-8")
    assert "source_url" not in content
    assert "http://" not in content
    assert "https://" not in content
    assert "fetch(\"./data/" in content


def test_homepage_loads_renderer_and_render_targets() -> None:
    content = HOME.read_text(encoding="utf-8")
    assert "./public-dashboard.js?v=20260525" in content
    assert "homepage-kpis" in content
    assert "issue-ranking-list" in content
    assert "hotspot-cards" in content
    assert "data-status-grid" in content
