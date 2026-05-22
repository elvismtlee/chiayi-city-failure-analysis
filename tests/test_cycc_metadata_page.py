import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "cycc-metadata.html"
SCRIPT = DASHBOARD_DIR / "cycc-metadata.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"
MINUTES_JSON = DASHBOARD_DIR / "data" / "cycc_minutes_metadata.json"
VIDEOS_JSON = DASHBOARD_DIR / "data" / "cycc_question_video_metadata.json"


def test_cycc_metadata_page_files_exist() -> None:
    assert HTML.exists()
    assert SCRIPT.exists()
    assert MINUTES_JSON.exists()
    assert VIDEOS_JSON.exists()


def test_cycc_metadata_page_discloses_internal_manual_review() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "議會公開 metadata 審核台" in content
    assert "internal metadata" in content
    assert "manual review required" in content
    assert "manual publishing only" in content


def test_cycc_metadata_page_reads_dashboard_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/cycc_minutes_metadata.json" in content
    assert "./data/cycc_question_video_metadata.json" in content
    assert "./data/cycc_public_records_crawl_report.json" in content
    assert "renderTable" in content


def test_cycc_metadata_page_is_in_site_map_and_nav() -> None:
    site_map = SITE_MAP.read_text(encoding="utf-8")
    shared_nav = SHARED_NAV.read_text(encoding="utf-8")
    assert "./cycc-metadata.html" in site_map
    assert "./cycc-metadata.html" in shared_nav
    assert "議會公開 metadata" in site_map
    assert "議會公開 metadata" in shared_nav


def test_cycc_metadata_json_total_count_is_141() -> None:
    minutes = json.loads(MINUTES_JSON.read_text(encoding="utf-8"))
    videos = json.loads(VIDEOS_JSON.read_text(encoding="utf-8"))
    assert minutes["total_count"] == 10
    assert videos["total_count"] == 131
    assert minutes["total_count"] + videos["total_count"] == 141
