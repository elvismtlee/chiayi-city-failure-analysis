from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / 'dashboard' / 'index.html'


def test_home_page_shows_city_data_dashboard() -> None:
    content = HOME.read_text(encoding='utf-8')
    assert '嘉義市城市故障分析儀表板' in content
    assert 'CITY DATA DASHBOARD' in content
    assert '城市故障總覽' in content
    assert '原型案件數' in content
    assert '12,458' in content
    assert '質詢紀錄數' in content
    assert '386' in content
    assert '城市熱點' in content
    assert '18' in content
    assert '最主要議題' in content
    assert '交通' in content
    assert '文化路商圈' in content
    assert '市場周邊' in content
    assert '學校周邊' in content
    assert './map.html' in content
    assert './source-verification-workspace.html' in content
    assert './command-center.html' in content
    assert './project-landing.html' in content
    assert 'no live crawler' in content
    assert 'no source_url requests' in content
    assert 'approved_for_crawling' in content
    assert './shared-nav.js?v=20260523-navux' in content
