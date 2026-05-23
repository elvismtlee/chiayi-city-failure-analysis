from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
DASHBOARD_PAGES = [
    "index.html",
    "map.html",
    "geocoding-review.html",
    "cycc-review.html",
    "insights.html",
    "sources.html",
    "methodology.html",
    "reports.html",
    "404.html",
]
PUBLISH_PAGES = ["public-review.html", "approved-materials.html", "daily-execution.html"]


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
        "./geocoding-review.html",
        "./cycc-review.html",
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


def test_shared_nav_contains_geocoding_review_label() -> None:
    content = (DASHBOARD_DIR / "shared-nav.js").read_text(encoding="utf-8")
    assert "座標審核" in content
    assert "geocoding-review.html" in content


def test_shared_nav_contains_cycc_review_label() -> None:
    content = (DASHBOARD_DIR / "shared-nav.js").read_text(encoding="utf-8")
    assert "CYCC公開資料" in content
    assert "cycc-review.html" in content


def test_shared_nav_contains_disclosure() -> None:
    content = (DASHBOARD_DIR / "shared-nav.js").read_text(encoding="utf-8")
    assert "DASHBOARD_DISCLOSURE" in content
    assert "不代表完整民意調查" in content


def test_shared_nav_uses_two_level_grouped_navigation() -> None:
    content = (DASHBOARD_DIR / "shared-nav.js").read_text(encoding="utf-8")
    assert "dashboard-nav-main" in content
    assert "dashboard-nav-sub" in content
    assert "dashboard-nav-tab" in content
    assert "dashboard-nav-link" in content
    assert "grid-template-columns:repeat(5" in content
    for label in ["總覽", "資料審核", "內容產出", "發布管理", "系統說明"]:
        assert label in content


def test_key_pages_bust_shared_nav_cache() -> None:
    for page in ["index.html", "weekly-summary.html", "policy-drafts.html"]:
        content = (DASHBOARD_DIR / page).read_text(encoding="utf-8")
        assert './shared-nav.js?v=20260523-navux' in content


def test_publish_pages_use_shared_nav_style() -> None:
    for page in PUBLISH_PAGES:
        content = (DASHBOARD_DIR / page).read_text(encoding="utf-8")
        assert '.nav{display:block' in content
        assert './shared-nav.js?v=20260523-navux' in content
        assert '.nav{display:flex' not in content


def test_dashboard_pages_load_shared_nav_script() -> None:
    for page in DASHBOARD_PAGES:
        content = (DASHBOARD_DIR / page).read_text(encoding="utf-8")
        assert './shared-nav.js' in content, f"{page} should load shared-nav.js"


def test_primary_pages_keep_nav_container() -> None:
    for page in DASHBOARD_PAGES[:-1]:
        content = (DASHBOARD_DIR / page).read_text(encoding="utf-8")
        assert '<nav class="nav">' in content, f"{page} should keep nav container"
