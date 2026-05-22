import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_command_center_page_assets_and_navigation_exist() -> None:
    html = (ROOT / "dashboard" / "command-center.html").read_text(encoding="utf-8")
    js = (ROOT / "dashboard" / "command-center.js").read_text(encoding="utf-8")
    site_map = json.loads((ROOT / "dashboard" / "data" / "site_map.json").read_text(encoding="utf-8"))
    shared_nav = (ROOT / "dashboard" / "shared-nav.js").read_text(encoding="utf-8")

    assert "command_center_overview.json" in js
    assert "總控台" in json.dumps(site_map, ensure_ascii=False)
    assert "總控台" in shared_nav
    assert "內部" in html
    assert "不自動發布" in html
    assert "民調" not in html.replace("不是民調", "")
    assert "支持度調查" not in html.replace("不是支持度調查", "")
