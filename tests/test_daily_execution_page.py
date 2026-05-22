from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "daily-execution.html"
SCRIPT = DASHBOARD_DIR / "daily-execution.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_daily_execution_page_files_exist() -> None:
    assert HTML.exists()
    assert SCRIPT.exists()


def test_daily_execution_page_discloses_internal_scope() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "每日執行" in content
    assert "internal" in content
    assert "manual review" in content
    assert "manual publishing" in content


def test_daily_execution_renderer_reads_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/daily_execution_list.json" in content
    assert "bootDailyExecution" in content


def test_daily_execution_page_is_in_site_map_and_nav() -> None:
    assert "./daily-execution.html" in SITE_MAP.read_text(encoding="utf-8")
    assert "./daily-execution.html" in SHARED_NAV.read_text(encoding="utf-8")
