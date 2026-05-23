from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260523_crawler_specs.md'


def test_crawler_spec_progress_note() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #159' in content
    assert 'open-data-crawler-specs.html' in content
    assert 'open_data_crawler_spec_drafts.json' in content
    assert 'total_count：10' in content
    assert 'crawler_execution_allowed：false' in content
    assert 'no_live_crawler' in content
    assert 'feat/open-data-human-review-workbook' in content
