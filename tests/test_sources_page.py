from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sources_page_public_content() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    assert '資料來源' in content
    assert '資料透明原則' in content
    assert '資料來源總覽' in content
    assert '目前已有原型資料' in content
    assert '官方資料來源盤點' in content
    assert '資料安全邊界' in content
    assert 'prototype dashboard' in content
    assert 'approved_for_crawling' in content


def test_sources_page_data_files_and_links() -> None:
    content = (ROOT / 'dashboard' / 'sources.html').read_text(encoding='utf-8')
    for text in ['dashboard_summary.json', 'hotspots.json', 'hotspots.geojson', 'issue_trends.json']:
        assert text in content
    for link in ['./index.html', './map.html', './command-center.html', './methodology.html', './health-check.html', './open-data-inventory.html']:
        assert link in content
