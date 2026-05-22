from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "video-scripts.html"
SCRIPT = DASHBOARD_DIR / "video-scripts.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_video_scripts_page_files_exist() -> None:
    assert HTML.exists()
    assert SCRIPT.exists()


def test_video_scripts_page_discloses_internal_review_scope() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "短影音腳本草稿清單" in content
    assert "內部短影音腳本草稿" in content
    assert "不自動發布" in content
    assert "人工審核" in content
    assert "不得使用深偽、冒充或誤導剪輯" in content


def test_video_scripts_renderer_reads_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/short_video_script_drafts.json" in content
    assert "bootVideoScripts" in content


def test_video_scripts_page_is_in_site_map_and_nav() -> None:
    assert "./video-scripts.html" in SITE_MAP.read_text(encoding="utf-8")
    assert "./video-scripts.html" in SHARED_NAV.read_text(encoding="utf-8")
