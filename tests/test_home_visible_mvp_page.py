from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / 'dashboard' / 'index.html'


def test_home_page_shows_public_city_dashboard() -> None:
    content = HOME.read_text(encoding='utf-8')
    assert '嘉義市城市問題儀表板' in content
    assert 'CITY DATA DASHBOARD' in content
    assert '原型案件數' in content
    assert '12,458' in content
    assert '質詢紀錄數' in content
    assert '386' in content
    assert '城市熱點' in content
    assert '18' in content
    assert '最大議題' in content
    assert '交通' in content
    assert '議題排行' in content
    assert '熱點分析' in content
    assert '資料來源接入狀態' in content
    assert '文化路商圈' in content
    assert '市場周邊' in content
    assert '學校周邊' in content
    assert '商圈動線與停車熱點專案' in content
    assert 'dashboard_summary.json' in content
    assert 'issue_trends.json' in content
    assert 'hotspots.json' in content
    assert 'dashboard_health_check.json' in content
    assert 'prototype dashboard' in content
    assert 'no live crawler' in content
    assert 'approved_for_crawling' in content
    assert './map.html' in content
    assert './source-verification-workspace.html' in content
    assert './command-center.html' in content
    assert './project-landing.html' in content
    assert './sources.html' in content
    assert './health-check.html' in content
    assert './public-dashboard.js' in content
    assert './shared-nav.js?v=20260523-navux' in content
