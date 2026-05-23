from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sources_links_to_open_data_inventory() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-inventory.html' in content
    assert '前往官方開放資料 URL 盤點' in content


def test_sources_links_to_open_data_review_queue() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-review.html' in content
    assert '前往官方資料 URL 人工審核' in content


def test_sources_links_to_open_data_readiness() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-readiness.html' in content
    assert '前往官方資料 Readiness 評分' in content


def test_sources_links_to_open_data_top10_tasks() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-top10-tasks.html' in content
    assert '前往 Top 10 官方資料審核任務' in content


def test_sources_links_to_open_data_crawler_specs() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-crawler-specs.html' in content
    assert '前往 Crawler 規格草稿' in content
