from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260523_engineering_review.md'


def test_engineering_review_progress_note() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #162' in content
    assert 'open-data-engineering-review.html' in content
    assert 'open_data_engineering_review_checklist.json' in content
    assert 'total_count：10' in content
    assert 'engineering_review_allowed_count：0' in content
    assert 'crawler_execution_allowed：false' in content
    assert 'feat/open-data-review-session-planner' in content
