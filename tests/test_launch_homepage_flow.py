from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "dashboard" / "index.html"
LANDING = ROOT / "dashboard" / "project-landing.html"
WORKSPACE = ROOT / "dashboard" / "source-verification-workspace.html"
SHARED_NAV = ROOT / "dashboard" / "shared-nav.js"


def test_launch_homepage_flow_prioritizes_main_entry_points() -> None:
    content = HOME.read_text(encoding="utf-8")
    assert "MVP 上線入口" in content
    assert "資料源檢查工作台" in content
    assert "./project-landing.html" in content
    assert "./source-verification-workspace.html" in content
    assert "./command-center.html" in content
    assert "./open-data-day1-operation-board.html" in content


def test_launch_homepage_flow_keeps_nav_polish_and_clear_starting_points() -> None:
    nav_content = SHARED_NAV.read_text(encoding="utf-8")
    assert "資料源檢查工作台" in nav_content
    assert ".dashboard-nav-tab.active,.dashboard-nav-link.active" in nav_content
    workspace = WORKSPACE.read_text(encoding="utf-8")
    for field in [
        "source_title",
        "source_owner",
        "source_url",
        "is_official_source",
        "data_format",
        "visible_fields",
        "privacy_risk",
        "recommended_next_action",
    ]:
        assert field in workspace
    landing = LANDING.read_text(encoding="utf-8")
    assert "現在怎麼開始" in landing
