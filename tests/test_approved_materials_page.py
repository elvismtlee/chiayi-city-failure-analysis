from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "approved-materials.html"
SCRIPT = DASHBOARD_DIR / "approved-materials.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_approved_materials_page_files_exist() -> None:
    assert HTML.exists()
    assert SCRIPT.exists()


def test_approved_materials_page_discloses_manual_publishing() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "已核准素材" in content
    assert "manual publishing" in content
    assert "人工手動發布" in content
    assert "發布前仍需再次確認" in content


def test_approved_materials_renderer_reads_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/approved_materials_sample.json" in content
    assert "bootApprovedMaterials" in content


def test_approved_materials_page_is_in_site_map_and_nav() -> None:
    assert "./approved-materials.html" in SITE_MAP.read_text(encoding="utf-8")
    assert "./approved-materials.html" in SHARED_NAV.read_text(encoding="utf-8")
