from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'dashboard' / 'open-data-top10-tasks.html'


def test_open_data_top10_tasks_page() -> None:
    content = PAGE.read_text(encoding='utf-8')
    assert 'Top 10 官方資料人工審核任務' in content
    assert 'openDataTop10Search' in content
    assert 'openDataTop10TopicGroup' in content
    assert 'openDataTop10Priority' in content
    assert 'openDataTop10Status' in content
    assert 'manual review' in content
    assert 'no auto publish' in content
    assert 'no live crawler' in content
    assert './shared-nav.js?v=20260523-navux' in content
