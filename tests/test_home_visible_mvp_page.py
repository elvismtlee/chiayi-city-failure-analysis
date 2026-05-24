from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / 'dashboard' / 'index.html'


def test_home_page_shows_city_data_dashboard() -> None:
    content = HOME.read_text(encoding='utf-8')
    assert '嘉義市城市問題儀表板' in content
    assert '用公開資料與原型資料' in content
    assert '原型案件數' in content
    assert '12,458' in content
    assert '質詢紀錄數' in content
    assert '386' in content
    assert '城市熱點' in content
    assert '18' in content
    assert '最大議題' in content
    assert '交通' in content
    assert '文化路商圈' in content
    assert '市場周邊' in content
    assert '學校周邊' in content
    assert '商圈動線與停車熱點專案' in content
    assert '市場周邊環境改善與卸貨規劃' in content
    assert '通學步道與接送區改善' in content
    assert 'prototype dashboard' in content
    assert 'no live crawler' in content
    assert 'no source_url requests' in content
    assert 'approved_for_crawling' in content
    assert './map.html' in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_home_page_keeps_secondary_dashboard_links() -> None:
    content = HOME.read_text(encoding='utf-8')
    assert './source-verification-workspace.html' in content
    assert './command-center.html' in content
    assert './project-landing.html' in content
    assert './open-data-day1-operation-board.html' in content
    assert './shared-nav.js?v=20260523-navux' in content
