from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "filming-checklists.html"
SCRIPT = DASHBOARD_DIR / "filming-checklists.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_filming_checklists_page_files_exist() -> None:
    assert HTML.exists()
    assert SCRIPT.exists()


def test_filming_checklists_page_discloses_internal_review_scope() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "拍攝清單候選" in content
    assert "內部拍攝清單" in content
    assert "不是自動發布內容" in content
    assert "人工確認" in content
    assert "不得偷拍、冒充或使用誤導剪輯" in content


def test_filming_checklists_renderer_reads_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/filming_checklists.json" in content
    assert "bootFilmingChecklists" in content


def test_filming_checklists_page_is_in_site_map_and_nav() -> None:
    assert "./filming-checklists.html" in SITE_MAP.read_text(encoding="utf-8")
    assert "./filming-checklists.html" in SHARED_NAV.read_text(encoding="utf-8")
