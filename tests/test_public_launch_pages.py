from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / 'dashboard'


def page(name: str) -> str:
    return (DASHBOARD / name).read_text(encoding='utf-8')


def test_public_pages_exist() -> None:
    for name in ['index.html', 'map.html', 'command-center.html', 'sources.html', 'methodology.html', 'health-check.html']:
        assert (DASHBOARD / name).exists()


def test_public_pages_have_public_titles() -> None:
    assert '嘉義市城市問題儀表板' in page('index.html')
    assert '城市熱點地圖' in page('map.html')
    assert '嘉義市城市資料總控台' in page('command-center.html')
    assert '資料來源' in page('sources.html')
    assert '城市故障分析方法論' in page('methodology.html')
    assert '網站與資料健康檢查' in page('health-check.html')


def test_public_pages_have_dashboard_content() -> None:
    home = page('index.html')
    assert '原型案件數' in home
    assert '議題排行' in home
    assert '文化路商圈' in home
    project = page('project-landing.html')
    assert '嘉義市城市問題儀表板專案總覽' in project
    assert '現在怎麼開始' in project
    map_page = page('map.html')
    assert 'Top 3 熱點行動建議' in map_page
    assert '地圖資料怎麼理解' in map_page
    sources = page('sources.html')
    assert '資料透明原則' in sources
    assert '目前已有原型資料' in sources
    assert '官方資料來源盤點' in sources


def test_shared_nav_prioritizes_public_pages() -> None:
    nav = page('shared-nav.js')
    for text in ['儀表板首頁', '城市熱點地圖', '總控台', '資料來源', '方法論', '健康檢查']:
        assert text in nav
    assert 'height:42px!important' in nav
    assert '.dashboard-nav-tab.active,.dashboard-nav-link.active' in nav
