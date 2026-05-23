from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260523_review_sessions.md'


def test_review_sessions_progress_note() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #165' in content
    assert 'open-data-review-sessions.html' in content
    assert 'open_data_review_session_planner.json' in content
    assert 'total_count：10' in content
    assert 'total_estimated_minutes：285' in content
    assert 'crawler_execution_allowed：false' in content
    assert 'feat/open-data-review-evidence-pack' in content
