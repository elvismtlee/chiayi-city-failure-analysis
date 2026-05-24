from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / 'dashboard'


def read_page(name: str) -> str:
    return (DASHBOARD / name).read_text(encoding='utf-8')


def test_project_landing_public_overview() -> None:
    content = read_page('project-landing.html')
    assert '公開展示頁' in content or '專案說明' in content
    assert '嘉義市城市問題儀表板專案總覽' in content
    assert '嘉義市城市問題儀表板' in content
    assert '現在已經能看什麼' in content
    assert '現在怎麼開始' in content
    assert '主要功能' in content
    assert '下一步會補什麼' in content
    assert './index.html' in content
    assert './map.html' in content
    assert './sources.html' in content


def test_not_found_page_links_public_pages() -> None:
    content = read_page('404.html')
    assert '頁面不存在' in content
    assert './index.html' in content
    assert './map.html' in content
    assert './sources.html' in content
    assert './command-center.html' in content
    assert './methodology.html' in content
    assert './health-check.html' in content
