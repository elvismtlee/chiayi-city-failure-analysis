from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'dashboard' / 'open-data-inventory.html'


def test_open_data_inventory_page_has_required_ui() -> None:
    content = PAGE.read_text(encoding='utf-8')
    assert '嘉義市官方開放資料 URL 盤點' in content
    assert 'id="openDataSearch"' in content
    assert 'id="openDataTopicGroup"' in content
    assert 'manual review required' in content
    assert 'no auto publish' in content
    assert '不啟動 crawler' in content
    assert './shared-nav.js?v=20260523-navux' in content
