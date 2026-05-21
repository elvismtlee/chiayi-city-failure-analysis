from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"


def test_shared_nav_script_exists() -> None:
    path = DASHBOARD_DIR / "shared-nav.js"
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "DASHBOARD_NAV_ITEMS" in content
    assert "renderSharedNav" in content
    assert "renderSharedFooter" in content


def test_shared_nav_contains_required_pages() -> None:
    content = (DASHBOARD_DIR / "shared-nav.js").read_text(encoding="utf-8")
    for page in [
        "./index.html",
        "./insights.html",
        "./sources.html",
        "./methodology.html",
        "./reports.html",
    ]:
        assert page in content


def test_shared_nav_contains_disclosure() -> None:
    content = (DASHBOARD_DIR / "shared-nav.js").read_text(encoding="utf-8")
    assert "DASHBOARD_DISCLOSURE" in content
    assert "不代表完整民意調查" in content
