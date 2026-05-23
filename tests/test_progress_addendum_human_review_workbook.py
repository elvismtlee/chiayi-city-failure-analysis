from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260523_human_review_workbook.md'


def test_human_review_progress_note() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #161' in content
    assert 'open-data-human-review.html' in content
    assert 'total_count：10' in content
    assert 'crawler_execution_allowed：false' in content
