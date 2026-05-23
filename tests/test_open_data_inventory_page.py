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
    assert '不啟動 live crawler' in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_open_data_inventory_page_links_to_review_queue() -> None:
    content = PAGE.read_text(encoding='utf-8')
    assert './open-data-review.html' in content
    assert '進入 URL 人工審核佇列' in content


def test_open_data_inventory_page_links_to_readiness() -> None:
    content = PAGE.read_text(encoding='utf-8')
    assert './open-data-readiness.html' in content
    assert '查看 Readiness 評分' in content


def test_open_data_inventory_page_links_to_top10_tasks() -> None:
    content = PAGE.read_text(encoding='utf-8')
    assert './open-data-top10-tasks.html' in content
    assert '查看 Top 10 審核任務' in content
