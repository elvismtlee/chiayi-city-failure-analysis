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


def test_sources_links_to_open_data_human_review() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-human-review.html' in content
    assert '前往人工審核工作簿' in content


def test_sources_links_to_open_data_engineering_review() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-engineering-review.html' in content
    assert '前往工程審查清單' in content


def test_sources_links_to_open_data_review_sessions() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-review-sessions.html' in content
    assert '前往人工審核執行工作台' in content


def test_sources_links_to_open_data_review_evidence() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-review-evidence.html' in content
    assert '前往審核證據包' in content


def test_sources_links_to_open_data_manual_review_results() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-manual-review-results.html' in content
    assert '前往審核結果輸入表' in content


def test_sources_links_to_open_data_manual_review_sop() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-manual-review-sop.html' in content
    assert '前往人工審核 SOP' in content


def test_sources_links_to_open_data_manual_review_packets() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-manual-review-packets.html' in content
    assert '前往人工審核工作包' in content


def test_sources_links_to_open_data_manual_review_patches() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert './open-data-manual-review-patches.html' in content
    assert '前往回填 Patch 草稿' in content
