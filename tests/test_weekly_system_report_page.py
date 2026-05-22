import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_weekly_system_report_page_assets_and_navigation_exist() -> None:
    html = (ROOT / "dashboard" / "weekly-system-report.html").read_text(encoding="utf-8")
    js = (ROOT / "dashboard" / "weekly-system-report.js").read_text(encoding="utf-8")
    site_map = json.loads((ROOT / "dashboard" / "data" / "site_map.json").read_text(encoding="utf-8"))
    shared_nav = (ROOT / "dashboard" / "shared-nav.js").read_text(encoding="utf-8")

    assert "weekly_system_report.json" in js
    assert "每週系統報告" in json.dumps(site_map, ensure_ascii=False)
    assert "每週系統報告" in shared_nav
    assert "內部" in html
    assert "不自動發布" in html
