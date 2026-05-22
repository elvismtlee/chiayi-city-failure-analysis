from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "weekly-summary.html"
SCRIPT = DASHBOARD_DIR / "weekly-summary.js"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_weekly_summary_page_has_dashboard_layout() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "每週市政議題摘要草稿" in content
    assert "data-render=\"breadcrumb\"" in content
    assert "kpi-grid" in content
    assert "data-render=\"top-issues\"" in content
    assert "data-render=\"policy-topics\"" in content
    assert "data-render=\"needs-review\"" in content
    assert "不是民調" in content


def test_weekly_summary_renderer_builds_cards() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/weekly_summary_draft.json" in content
    assert "makeIssueCard" in content
    assert "makePolicyCard" in content
    assert "renderSourceFiles" in content


def test_shared_nav_has_grouped_navigation() -> None:
    content = SHARED_NAV.read_text(encoding="utf-8")
    for label in ["總覽", "資料審核", "內容產出", "發布管理", "系統說明"]:
        assert label in content
    assert "DASHBOARD_NAV_GROUPS" in content
