from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260523_open_data_review_queue.md'


def test_progress_addendum_records_open_data_review_queue() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #153' in content
    assert 'open-data-review.html' in content
    assert 'open_data_url_review_queue.json' in content
    assert '29 筆' in content
    assert 'no_live_crawler' in content
    assert 'feat/open-data-readiness-report' in content
