from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sources_links_to_open_data_inventory() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-inventory.html' in content
    assert '前往官方開放資料 URL 盤點' in content
