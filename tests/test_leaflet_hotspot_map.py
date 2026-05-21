from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"


def test_leaflet_map_page_exists() -> None:
    path = DASHBOARD_DIR / "map.html"
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "leaflet" in content.lower()
    assert "leaflet_hotspot_map" in content
    assert "./leaflet-map.js" in content
    assert "./shared-nav.js" in content


def test_leaflet_renderer_loads_hotspots_json() -> None:
    content = (DASHBOARD_DIR / "leaflet-map.js").read_text(encoding="utf-8")
    assert "./data/hotspots.json" in content
    assert "bootLeafletHotspotMap" in content
    assert "bindPopup" in content


def test_leaflet_renderer_has_prototype_coordinate_fallback() -> None:
    content = (DASHBOARD_DIR / "leaflet-map.js").read_text(encoding="utf-8")
    assert "FALLBACK_HOTSPOT_COORDS" in content
    assert "isPrototype" in content
    assert "prototype" in content


def test_leaflet_renderer_uses_openstreetmap_tiles() -> None:
    content = (DASHBOARD_DIR / "leaflet-map.js").read_text(encoding="utf-8")
    assert "tile.openstreetmap.org" in content
    assert "OpenStreetMap contributors" in content
