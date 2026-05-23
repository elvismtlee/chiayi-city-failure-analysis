from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260523_manual_review_sop_and_nav.md'


def test_manual_review_sop_and_nav_progress_note() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #174' in content
    assert 'PR #176' in content
    assert 'open-data-manual-review-sop.html' in content
    assert 'open_data_manual_review_sop.json' in content
    assert 'total_tasks：10' in content
    assert 'height：42px' in content
    assert 'status ok' in content
    assert 'feat/open-data-manual-review-execution-packets' in content
