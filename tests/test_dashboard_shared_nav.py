from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
DASHBOARD_PAGES = [
    "index.html",
    "map.html",
    "insights.html",
    "sources.html",
    "methodology.html",
    "reports.html",
    "404.html",
]


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
        "./map.html",
        "./insights.html",
        "./sources.html",
        "./methodology.html",
        "./reports.html",
    ]:
        assert page in content


def test_shared_nav_contains_hotspot_map_label() -> None:
    content = (DASHBOARD_DIR / "shared-nav.js").read_text(encoding="utf-8")
    assert "城市熱點地圖" in content
    assert "map.html" in content


def test_shared_nav_contains_disclosure() -> None:
    content = (DASHBOARD_DIR / "shared-nav.js").read_text(encoding="utf-8")
    assert "DASHBOARD_DISCLOSURE" in content
    assert "不代表完整民意調查" in content


def test_dashboard_pages_load_shared_nav_script() -> None:
    for page in DASHBOARD_PAGES:
        content = (DASHBOARD_DIR / page).read_text(encoding="utf-8")
        assert './shared-nav.js' in content, f"{page} should load shared-nav.js"


def test_primary_pages_keep_nav_container() -> None:
    for page in DASHBOARD_PAGES[:-1]:
        content = (DASHBOARD_DIR / page).read_text(encoding="utf-8")
        assert '<nav class="nav">' in content, f"{page} should keep nav container"
