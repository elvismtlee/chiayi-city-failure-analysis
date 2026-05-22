from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "social-drafts.html"
SCRIPT = DASHBOARD_DIR / "social-drafts.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_social_drafts_page_files_exist() -> None:
    assert HTML.exists()
    assert SCRIPT.exists()


def test_social_drafts_page_discloses_internal_review_scope() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "社群文案草稿清單" in content
    assert "內部文案草稿" in content
    assert "不自動發布" in content
    assert "人工審核" in content


def test_social_drafts_renderer_reads_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/social_post_drafts.json" in content
    assert "bootSocialDrafts" in content


def test_social_drafts_page_is_in_site_map_and_nav() -> None:
    assert "./social-drafts.html" in SITE_MAP.read_text(encoding="utf-8")
    assert "./social-drafts.html" in SHARED_NAV.read_text(encoding="utf-8")
