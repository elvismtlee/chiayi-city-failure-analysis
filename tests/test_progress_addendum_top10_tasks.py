from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260523_top10_tasks.md'


def test_top10_progress_note() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #157' in content
    assert 'open-data-top10-tasks.html' in content
    assert 'total_count：10' in content
    assert 'P1：4' in content
    assert 'no_live_crawler' in content
