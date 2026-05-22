from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "public-review.html"
SCRIPT = DASHBOARD_DIR / "public-review.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_public_review_page_files_exist() -> None:
    assert HTML.exists()
    assert SCRIPT.exists()


def test_public_review_page_discloses_review_requirement() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "公開審核" in content
    assert "未通過人工審核，不可公開使用" in content
    assert "needs human review" in content
    assert "manual publishing" in content


def test_public_review_renderer_reads_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/public_material_review_queue.json" in content
    assert "bootPublicReview" in content


def test_public_review_page_is_in_site_map_and_nav() -> None:
    assert "./public-review.html" in SITE_MAP.read_text(encoding="utf-8")
    assert "./public-review.html" in SHARED_NAV.read_text(encoding="utf-8")
