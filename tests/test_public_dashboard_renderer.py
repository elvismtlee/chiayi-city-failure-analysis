from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard"


def test_public_dashboard_renderer_exists() -> None:
    path = DASHBOARD / "public-dashboard.js"
    assert path.exists()


def test_public_dashboard_renderer_contains_required_functions_and_data_paths() -> None:
    content = (DASHBOARD / "public-dashboard.js").read_text(encoding="utf-8")
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


def test_public_dashboard_renderer_stays_local_only() -> None:
    content = (DASHBOARD / "public-dashboard.js").read_text(encoding="utf-8")
    assert "source_url" not in content
    assert "http://" not in content
    assert "https://" not in content
    assert "api.github.com" not in content
    assert "raw.githubusercontent.com" not in content


def test_index_loads_public_dashboard_renderer_and_render_targets() -> None:
    content = (DASHBOARD / "index.html").read_text(encoding="utf-8")
    for text in [
        "./public-dashboard.js",
        "homepage-kpis",
        "issue-ranking",
        "hotspot-cards",
        "data-status",
    ]:
        assert text in content
