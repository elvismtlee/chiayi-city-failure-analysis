from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260523_evidence_pack.md'


def test_evidence_pack_progress_note() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #169' in content
    assert 'PR #170' in content
    assert 'open-data-review-evidence.html' in content
    assert 'open_data_review_evidence_pack.json' in content
    assert 'total_count：10' in content
    assert 'valid_json true' in content
    assert 'status：ok' in content
    assert 'feat/open-data-manual-review-result-template' in content
