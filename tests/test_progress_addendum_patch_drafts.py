from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260524_patch_drafts.md'


def test_patch_drafts_progress_note() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #180' in content
    assert 'open-data-manual-review-patches.html' in content
    assert 'open_data_manual_review_result_patch_drafts.json' in content
    assert 'day_1_patch_drafts.md' in content
    assert 'day_2_patch_drafts.md' in content
    assert 'day_3_patch_drafts.md' in content
    assert 'total_count：10' in content
    assert 'sample_only: true' in content
    assert 'feat/open-data-day1-sample-manual-review-results' in content
