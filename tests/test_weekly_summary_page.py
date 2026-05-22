from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "weekly-summary.html"
SCRIPT = DASHBOARD_DIR / "weekly-summary.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_weekly_summary_page_files_exist() -> None:
    assert HTML.exists()
    assert SCRIPT.exists()


def test_weekly_summary_page_discloses_internal_draft_scope() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "每週市政議題摘要草稿" in content
    assert "不是正式結論" in content
    assert "不代表完整正式資料庫" in content
    assert "人工審核" in content


def test_weekly_summary_renderer_reads_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/weekly_summary_draft.json" in content
    assert "bootWeeklySummary" in content
    assert "renderSummary" in content


def test_weekly_summary_page_has_render_targets() -> None:
    content = HTML.read_text(encoding="utf-8")
    for target in [
        'data-stat="period"',
        'data-stat="total"',
        'data-stat="departments"',
        'data-stat="keywords"',
        'data-render="top-issues"',
        'data-render="policy-topics"',
        'data-render="needs-review"',
        'data-render="source-files"',
    ]:
        assert target in content


def test_weekly_summary_page_is_in_site_map_and_nav() -> None:
    assert "./weekly-summary.html" in SITE_MAP.read_text(encoding="utf-8")
    assert "./weekly-summary.html" in SHARED_NAV.read_text(encoding="utf-8")
