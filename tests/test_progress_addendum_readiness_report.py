from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260523_readiness_report.md'


def test_progress_addendum_records_readiness_report() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #155' in content
    assert 'open-data-readiness.html' in content
    assert 'open_data_readiness_report.json' in content
    assert 'total_count：29' in content
    assert 'high：16' in content
    assert 'internal_readiness_report' in content
    assert 'no_live_crawler' in content
    assert 'feat/open-data-top10-review-tasks' in content
