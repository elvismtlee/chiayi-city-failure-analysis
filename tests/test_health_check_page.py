import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_health_check_page_assets_and_navigation_exist() -> None:
    html = (ROOT / "dashboard" / "health-check.html").read_text(encoding="utf-8")
    js = (ROOT / "dashboard" / "health-check.js").read_text(encoding="utf-8")
    site_map = json.loads((ROOT / "dashboard" / "data" / "site_map.json").read_text(encoding="utf-8"))
    shared_nav = (ROOT / "dashboard" / "shared-nav.js").read_text(encoding="utf-8")

    assert "dashboard_health_check.json" in js
    assert "健康檢查" in json.dumps(site_map, ensure_ascii=False)
    assert "健康檢查" in shared_nav
    assert "內部" in html
    assert "不自動發布" in html
