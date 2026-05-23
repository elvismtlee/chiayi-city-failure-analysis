from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / 'dashboard' / 'index.html'


def test_home_page_shows_visible_day1_progress() -> None:
    content = HOME.read_text(encoding='utf-8')
    assert '嘉義城市故障分析資料庫' in content
    assert 'VISIBLE MVP' in content
    assert 'Day 1 審核表單' in content
    assert '人工審核工作包' in content
    assert '回填 Patch 草稿' in content
    assert '目前狀態' in content
    assert '內部人工審核階段' in content
    assert './open-data-day1-review-form.html' in content
    assert './open-data-manual-review-packets.html' in content
    assert './open-data-manual-review-patches.html' in content
    assert './shared-nav.js?v=20260523-navux' in content
