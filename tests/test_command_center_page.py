import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_command_center_page_is_public_readable_and_uses_local_data() -> None:
    html = (ROOT / "dashboard" / "command-center.html").read_text(encoding="utf-8")
    js = (ROOT / "dashboard" / "command-center.js").read_text(encoding="utf-8")
    site_map = json.loads((ROOT / "dashboard" / "data" / "site_map.json").read_text(encoding="utf-8"))

    assert "嘉義市城市資料總控台" in html
    assert "目前可用資料" in html
    assert "目前可用頁面" in html
    assert "資料接入狀態" in html
    assert "下一步補資料" in html
    assert "index.html" in html
    assert "map.html" in html
    assert "sources.html" in html
    assert "source-verification-workspace.html" in html
    assert "no live crawler" in html
    assert "approved_for_crawling" in html
    assert "./command-center.js?v=20260524-control-room" in html
    assert "renderControlRoomKpis" in js
    assert "renderAvailablePages" in js
    assert "renderDataStatus" in js
    assert "renderNextDataCards" in js
    assert "command_center_overview.json" in js
    assert "dashboard_summary.json" in js
    assert "hotspots.json" in js
    assert "issue_trends.json" in js
    assert "dashboard_health_check.json" in js
    assert "open_data_url_inventory.json" in js
    assert any(item.get("path") == "./command-center.html" for item in site_map)
