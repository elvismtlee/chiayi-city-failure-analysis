from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260523_manual_review_results.md'


def test_manual_review_results_progress_note() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #171' in content
    assert 'open-data-manual-review-results.html' in content
    assert 'open_data_manual_review_result_template.json' in content
    assert 'total_count：10' in content
    assert 'result_status：not_started 10' in content
    assert 'crawler_execution_allowed：false' in content
    assert 'feat/open-data-manual-review-sop' in content
