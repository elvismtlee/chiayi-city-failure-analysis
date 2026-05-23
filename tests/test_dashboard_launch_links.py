import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard"
WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"
SITE_MAP = ROOT / "dashboard" / "data" / "site_map.json"
INDEX = DASHBOARD / "index.html"
SHARED_NAV = DASHBOARD / "shared-nav.js"


def test_launch_entry_pages_and_pages_files_exist() -> None:
    for path in [
        DASHBOARD / "index.html",
        DASHBOARD / "project-landing.html",
        DASHBOARD / "source-verification-workspace.html",
        DASHBOARD / "command-center.html",
        DASHBOARD / "open-data-day1-operation-board.html",
        DASHBOARD / ".nojekyll",
        WORKFLOW,
    ]:
        assert path.exists(), f"Missing launch asset: {path}"


def test_pages_workflow_uses_dashboard_artifact_deploy_flow() -> None:
    content = WORKFLOW.read_text(encoding="utf-8")
    assert "actions/configure-pages" in content
    assert "actions/upload-pages-artifact" in content
    assert "actions/deploy-pages" in content
    assert "path: './dashboard'" in content
    assert "branches:" in content
    assert "- main" in content
    assert "dashboard/**" in content


def test_index_contains_four_main_launch_entry_links() -> None:
    content = INDEX.read_text(encoding="utf-8")
    for link in [
        "./project-landing.html",
        "./source-verification-workspace.html",
        "./command-center.html",
        "./open-data-day1-operation-board.html",
    ]:
        assert link in content


def test_shared_nav_keeps_main_launch_entries_and_button_style() -> None:
    content = SHARED_NAV.read_text(encoding="utf-8")
    for label in [
        "公開展示頁",
        "資料源檢查工作台",
        "總控台",
        "Day1操作看板",
    ]:
        assert label in content
    assert "height:42px!important" in content
    assert "font-size:16px!important" in content
    assert "line-height:1!important" in content
    assert "padding:0 16px!important" in content
    assert ".dashboard-nav-tab.active,.dashboard-nav-link.active" in content


def test_site_map_includes_main_launch_pages() -> None:
    site_map = json.loads(SITE_MAP.read_text(encoding="utf-8"))
    paths = {item["path"] for item in site_map}
    for path in [
        "./index.html",
        "./project-landing.html",
        "./source-verification-workspace.html",
        "./command-center.html",
        "./open-data-day1-operation-board.html",
    ]:
        assert path in paths
