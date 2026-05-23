from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / 'dashboard' / 'index.html'


def test_home_page_shows_visible_mvp_progress() -> None:
    content = HOME.read_text(encoding='utf-8')
    assert '嘉義市城市故障分析資料庫｜MVP 上線入口' in content
    assert 'MVP 上線入口' in content
    assert '公開展示頁已完成' in content
    assert '資料源檢查工作台已完成' in content
    assert '成果總控台已完成' in content
    assert 'GitHub Pages 上線準備已完成' in content
    assert '公開展示頁' in content
    assert './project-landing.html' in content
    assert './source-verification-workspace.html' in content
    assert './command-center.html' in content
    assert './open-data-day1-operation-board.html' in content
    assert './shared-nav.js?v=20260523-navux' in content
