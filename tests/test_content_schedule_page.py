from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "content-schedule.html"
SCRIPT = DASHBOARD_DIR / "content-schedule.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_content_schedule_page_files_exist() -> None:
    assert HTML.exists()
    assert SCRIPT.exists()


def test_content_schedule_page_discloses_internal_scope() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "內容排程" in content
    assert "internal" in content
    assert "manual review" in content
    assert "manual publishing" in content


def test_content_schedule_renderer_reads_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/content_schedule.json" in content
    assert "bootContentSchedule" in content


def test_content_schedule_page_is_in_site_map_and_nav() -> None:
    assert "./content-schedule.html" in SITE_MAP.read_text(encoding="utf-8")
    assert "./content-schedule.html" in SHARED_NAV.read_text(encoding="utf-8")
