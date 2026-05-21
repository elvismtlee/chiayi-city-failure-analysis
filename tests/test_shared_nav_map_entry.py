from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHARED_NAV = ROOT / "dashboard" / "shared-nav.js"


def test_shared_nav_includes_hotspot_map_page() -> None:
    content = SHARED_NAV.read_text(encoding="utf-8")
    assert "./map.html" in content
    assert "map.html" in content
    assert "城市熱點地圖" in content
