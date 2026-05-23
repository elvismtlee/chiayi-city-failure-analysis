from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260524_day1_sample_results.md'


def test_day1_sample_progress_note() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #182' in content
    assert 'open-data-day1-sample-results.html' in content
    assert 'open_data_day1_sample_manual_review_results.json' in content
    assert 'total_count：3' in content
    assert 'sample_only：true' in content
    assert 'not_actual_review_result：true' in content
    assert 'feat/open-data-day1-manual-review-form-draft' in content
